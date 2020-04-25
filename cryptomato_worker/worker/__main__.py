import logging
import multiprocessing
import os
import signal
import sys
from concurrent import futures

import grpc

from .evaluation import Experiment_APIServicer, Experiment_APIServiceAuthValidationInterceptor
from .manager import ManagerServicer
from .protos import api_pb2_grpc, private_api_pb2_grpc
from .sandbox import SandboxExecServicer, SANDBOX_UID, SANDBOX_GID


def serve_sandbox_server():
    sandbox_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max(1, multiprocessing.cpu_count() // 2))
    )
    private_api_pb2_grpc.add_SandboxExecServicer_to_server(SandboxExecServicer(), sandbox_server)
    sandbox_server.add_insecure_port('unix:///var/run/cryptomato/sandbox.sock')
    sandbox_server.start()
    os.chown('/var/run/cryptomato/sandbox.sock', os.getuid(), SANDBOX_GID + 1)
    os.chmod('/var/run/cryptomato/sandbox.sock', 0o660)
    print('sandbox_server started!')
    sandbox_server.wait_for_termination()


def serve_misc_server():
    eval_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=1024),
        interceptors=(Experiment_APIServiceAuthValidationInterceptor(),),
    )
    api_pb2_grpc.add_Experiment_APIServicer_to_server(Experiment_APIServicer(), eval_server)
    eval_server.add_insecure_port('unix:///var/run/cryptomato/api.sock')
    eval_server.start()
    os.chown('/var/run/cryptomato/api.sock', os.getuid(), SANDBOX_GID)
    os.chmod('/var/run/cryptomato/api.sock', 0o660)
    print('eval_server started!')

    manager_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max(1, multiprocessing.cpu_count() // 2))
    )
    private_api_pb2_grpc.add_ManagerServicer_to_server(ManagerServicer(), manager_server)
    manager_server.add_insecure_port('0.0.0.0:10000')
    manager_server.start()
    print('manager_server started!')

    eval_server.wait_for_termination()
    manager_server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'sandbox_server':
            serve_sandbox_server()
        elif sys.argv[1] == 'misc_server':
            serve_misc_server()
    else:
        import prctl, _prctl

        print('starting worker servers...')
        if not os.path.exists('/var/run/cryptomato'):
            os.mkdir('/var/run/cryptomato')
        os.chmod('/var/run/cryptomato', 0o1777)
        pid1 = os.fork()
        if not pid1:
            prctl.set_pdeathsig(signal.SIGKILL)
            # clear some CAP_INHERITABLE
            caps_to_keep = {
                prctl.CAP_SETUID,
                prctl.CAP_SETGID,
                prctl.CAP_CHOWN,
                prctl.CAP_KILL,
            }
            caps_to_clear = set(range(1024)).difference(caps_to_keep)
            _prctl.set_caps([], [], [], list(caps_to_clear), list(caps_to_clear), list(caps_to_clear))
            os.setsid()
            os.execl('/usr/bin/python3', '/usr/bin/python3', '-u', '-m', 'cryptomato_worker.worker', 'sandbox_server')
            sys.exit(0)
        pid2 = os.fork()
        if not pid2:
            prctl.set_pdeathsig(signal.SIGKILL)
            # clear all CAP_INHERITABLE
            _prctl.set_caps([], [], [], [], [], list(range(1024)))
            os.setsid()
            os.setgroups([SANDBOX_GID, SANDBOX_GID + 1, 1000])
            os.setresgid(SANDBOX_GID + 1, SANDBOX_GID + 1, SANDBOX_GID + 1)
            os.setresuid(SANDBOX_UID + 1, SANDBOX_UID + 1, SANDBOX_UID + 1)
            os.execl('/usr/bin/python3', '/usr/bin/python3', '-u', '-m', 'cryptomato_worker.worker', 'misc_server')
            sys.exit(0)

        os.setgroups([])
        os.setresgid(SANDBOX_GID + 2000, SANDBOX_GID + 2000, SANDBOX_GID + 2000)
        os.setresuid(SANDBOX_UID + 2000, SANDBOX_UID + 2000, SANDBOX_UID + 2000)


        def sigterm_handler(_signo, _stack_frame):
            sys.exit(0)


        signal.signal(signal.SIGTERM, sigterm_handler)

        os.waitpid(pid1, 0)
        os.waitpid(pid2, 0)
