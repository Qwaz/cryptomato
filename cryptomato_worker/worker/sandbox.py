import json
import multiprocessing
import os
import signal
import socket
import struct
import subprocess
import tempfile
import traceback

import grpc
import pwd

from . import BASEPATH
from .protos import private_api_pb2
from .protos import private_api_pb2_grpc

__all__ = (
    'sandbox_py_exec', 'SANDBOX_UID', 'SANDBOX_GID',
    'SandboxExecServicer',
)

SANDBOX_USERNAME = 'nobody'
SANDBOX_UID = pwd.getpwnam(SANDBOX_USERNAME).pw_uid
SANDBOX_GID = pwd.getpwnam(SANDBOX_USERNAME).pw_gid

_processes = {}


def _sandbox_py_exec(
        code,
        timeout=30,
        check_output=False,
        nsjail_quiet=True,
        envs=None,
        rw_mounts=None,
        entrypoint=None,
):
    code_file = tempfile.NamedTemporaryFile(delete=False)
    if isinstance(code, str):
        code = code.encode('utf-8')
    code_file.write(code)
    code_file.flush()
    os.fchmod(code_file.fileno(), 0o640)
    os.fchown(code_file.fileno(), os.getuid(), SANDBOX_GID)

    argv = []
    argv += [
        '/usr/sbin/nsjail',
        '-Mo',
        '--disable_proc',
        '--iface_no_lo',
        '-t', '%d' % timeout,
        '--rlimit_cpu', '%d' % (timeout * 2),
        '--rlimit_nproc', '%d' % max(16, multiprocessing.cpu_count() // 2),
        '--seccomp_policy', BASEPATH + '/seccomp.policy',
    ]
    if nsjail_quiet:
        argv += ['--really_quiet']
    argv += [
        '--user', '%d:%d' % (SANDBOX_UID, SANDBOX_UID),
        '--group', '%d:%d' % (SANDBOX_GID, SANDBOX_GID),
    ]
    for d in ('/bin/', '/lib/', '/lib64/', '/usr/', '/sbin/'):
        argv += ['-R', d]
    if rw_mounts is not None:
        for rw_mount in rw_mounts:
            argv += ['-B', rw_mount]
    if envs is not None:
        for k, v in envs.items():
            argv += ['-E', '%s=%s' % (k, v)]
    if os.path.exists('/var/run/cryptomato/api.sock'):
        argv += ['-B', '/var/run/cryptomato/api.sock']
    argv += [
        '-T', '/dev/',
        '-T', '/tmp/',
        '-R', '/dev/urandom',
        '-B', '/dev/null',
        '-R', code_file.name + ':/tmp/user.py',
        '-R', BASEPATH + '/exposed_lib/:/tmp/cryptomato',
        '--',
        '/usr/bin/python3', '/tmp/user.py' if entrypoint is None else entrypoint
    ]
    if check_output:
        result = subprocess.check_output(argv, stderr=subprocess.STDOUT)
        code_file.close()
    else:
        ipc_in, ipc_out, stdout = socket.socketpair(), socket.socketpair(), tempfile.TemporaryFile()
        argv[1:1] = [
            '--pass_fd', str(ipc_in[1].fileno()),
            '--pass_fd', str(ipc_out[1].fileno()),
            '-E', 'IPC_IN=%d' % ipc_in[1].fileno(),
            '-E', 'IPC_OUT=%d' % ipc_out[1].fileno(),
        ]
        p = subprocess.Popen(argv, stdout=stdout, stderr=subprocess.STDOUT,
                             pass_fds=(ipc_in[1].fileno(), ipc_out[1].fileno()))
        ipc_in[1].close()
        ipc_out[1].close()
        result = ipc_in[0], ipc_out[0], stdout, p
    return result


def sandbox_py_exec(
        code,
        **kwargs
):
    with grpc.insecure_channel('unix:///var/run/cryptomato/sandbox.sock') as channel:
        stub = private_api_pb2_grpc.SandboxExecStub(channel)
        response = stub.Exec(private_api_pb2.ExecRequest(
            code=code,
            options=json.dumps(kwargs),
        ))
        channel.close()
        return json.loads(response.result)


# noinspection PyPep8Naming
class SandboxExecServicer(private_api_pb2_grpc.SandboxExecServicer):
    def __init__(self):
        assert (
                _sandbox_py_exec(
                    "print('hello world!')\n",
                    timeout=30,
                    check_output=True,
                ).decode('ascii') ==
                'hello world!\n'
        )

    def Exec(self, request, context):
        # noinspection PyBroadException
        try:
            options = json.loads(request.options)
            user_code_output = _sandbox_py_exec(
                request.code,
                **options,
            )
            if not options.get("check_output", False):
                secret = os.urandom(16).hex()
                _processes[secret] = user_code_output
                user_code_output = secret.encode()

            result = {
                'type': 'success',
                'output': user_code_output.decode('ascii'),
            }
        except subprocess.CalledProcessError as e:
            result = {
                'type': 'CalledProcessError',
                'message': e.output.decode('ascii')
            }
        except Exception as e:
            result = {
                'type': 'Exception',
                'message': traceback.format_exc(e)
            }
        return private_api_pb2.ExecReply(result=json.dumps(result))

    def WriteStdin(self, request, context):
        info = _processes.get(request.id)
        if info is None:
            res = False
            content = "Process not found: %r" % request.id
        else:
            ipc_in, ipc_out, _, _ = info
            try:
                payload = request.content.encode()
                ipc_in.send(struct.pack("<L", len(payload)))
                ipc_in.send(payload)
                length, = struct.unpack("<L", ipc_out.recv(4, socket.MSG_WAITALL))
                content = json.loads(ipc_out.recv(length, socket.MSG_WAITALL).decode())
                res = True
            except:
                content = traceback.format_exc()
                res = False
        return private_api_pb2.WriteStdinReply(result=json.dumps({"success": res, "content": content}))

    def Terminate(self, request, context):
        info = _processes.get(request.id)
        if info is None:
            content = "Process not found: %r" % request.id
        else:
            ipc_in, ipc_out, stdout, proc = info
            try:
                proc.kill()
                stdout.seek(0)
                content = stdout.read().decode()
                ipc_in.close()
                ipc_out.close()
                stdout.close()
            except:
                content = traceback.format_exc()
            del _processes[request.id]

        return private_api_pb2.TerminateReply(output=content)
