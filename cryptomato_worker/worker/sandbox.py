import json
import multiprocessing
import os
import socket
import subprocess
import tempfile
import traceback
import struct

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
        '-R', '/dev/urandom',
        '-B', '/dev/null',
        '-B', '/tmp:/tmp/',
        '-R', code_file.name + ':/tmp/user.py',
        '-R', BASEPATH + '/exposed_lib/:/tmp/cryptomato',
        '--',
        '/usr/bin/python3', '/tmp/user.py' if entrypoint is None else entrypoint
    ]
    if check_output:
        result = subprocess.check_output(argv, stderr=subprocess.STDOUT)
        code_file.close()
    else:
        stdin, stdout = socket.socketpair(), socket.socketpair()
        open("/tmp/cmd", "w").write(" ".join(argv))
        subprocess.Popen(argv, stdin=stdin[1], stdout=stdout[1])
        result = stdin[0], stdout[0]
    return result


def sandbox_py_exec(
        code,
        **kwargs
):
    with grpc.insecure_channel('unix:///var/run/cryptomato/sandbox.sock') as channel:
        stub = private_api_pb2_grpc.SandboxExecStub(channel)
        response = stub.SandboxExec(private_api_pb2.SandboxExecRequest(
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

    def SandboxExec(self, request, context):
        # noinspection PyBroadException
        try:
            options = json.loads(request.options)
            user_code_output = _sandbox_py_exec(
                request.code,
                **options,
            )
            if not options.get("check_output", False):
                secret = os.urandom(16).hex()
                stdin, stdout = user_code_output
                _processes[secret] = (stdin, stdout)
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
        return private_api_pb2.SandboxExecReply(result=json.dumps(result))

    def SandboxWriteStdin(self, request, context):
        stdin, stdout = _processes.get(request.id)
        content = None
        if stdin is None:
            res = False
            content = "Process not found: %r" % request.id
        else:
            try:
                payload = request.content.encode()
                stdin.send(struct.pack("<L", len(payload)))
                stdin.send(payload)
                length, = struct.unpack("<L", stdout.recv(4, socket.MSG_WAITALL))
                content = json.loads(stdout.recv(length, socket.MSG_WAITALL).decode())
                res = True
            except:
                content = traceback.format_exc()
                res = False
        return private_api_pb2.SandboxWriteStdinReply(result=json.dumps({"success": res, "content": content}))
