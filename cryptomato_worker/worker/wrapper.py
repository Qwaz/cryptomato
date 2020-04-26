import functools
import json
import os
import grpc

from .sandbox import sandbox_py_exec
from ..protos import private_api_pb2, private_api_pb2_grpc


class Wrapper:
    def serialize_arg(self, arg, context):
        raise NotImplementedError

    def serialize_args(self, args, kwargs):
        raise NotImplementedError

    def get_target(self, key):
        raise NotImplementedError

    def __getattr__(self, key):
        target = self.get_target(key)

        @functools.wraps(target)
        def handler(*args, **kwargs):
            args, kwargs = self.serialize_args(args, kwargs)
            return target(*args, **kwargs)

        return handler


class LocalWrapper(Wrapper):
    def __init__(self, module):
        self.module = module

    def serialize_arg(self, arg, _):
        return arg

    def serialize_args(self, args, kwargs):
        return args, kwargs

    def get_target(self, key):
        return self.module.__getattribute__(key)


class RPCWrapper(Wrapper):
    def __init__(self, code, envs):
        self.objects = {}
        self.visited = {}

        res = sandbox_py_exec(
            code,
            envs=envs,
            check_output=False,
            entrypoint='/tmp/cryptomato/main.py'
        )
        assert res.get(
            "output"), "Unexpected result from sandbox server: %r" % res
        self.process = res["output"]
        self.channel = grpc.insecure_channel(
            'unix:///var/run/cryptomato/sandbox.sock')

    def serialize_arg(self, arg):
        if isinstance(arg, (int, str, bytes)):
            return {"type": "primitive", "value": arg}
        if isinstance(arg, tuple):
            return {"type": "primitive", "value": [self.serialize_arg(_) for _ in arg]}
        if isinstance(arg, dict):
            return {"type": "primitive",
                    "value": {key: self.serialize_arg(value) for key, value in arg.items()}}
        if callable(arg):
            __id = os.urandom(16).hex()
            self.objects[__id] = arg

            return {"type": "rpc", "id": __id}
        if hasattr(arg, "exports"):
            return {"type": "class", "name": arg.__class__.__name__,
                    "value": {key: self.serialize_arg(getattr(arg, key)) for key in arg.exports}}

        raise Exception(
            "Unsupported argument types for serialization: %r %r" % (arg, dir(arg)))

    def query_obj(self, id):
        return self.objects.get(id)

    def serialize_args(self, args, kwargs):
        new_args = [self.serialize_arg(_) for _ in args]
        new_kwargs = {key: self.serialize_arg(value)
                      for key, value in kwargs.items()}
        return new_args, new_kwargs

    def _wrapper(self, key):
        def handler(*args, **kwargs):
            self.channel = grpc.insecure_channel(
                'unix:///var/run/cryptomato/sandbox.sock')
            stub = private_api_pb2_grpc.SandboxExecStub(self.channel)
            req = private_api_pb2.WriteStdinRequest(id=self.process, content=json.dumps({
                "args": args,
                "kwargs": kwargs,
                "name": key
            }))
            res = json.loads(stub.WriteStdin(req).result)
            assert res["success"] == True, "Call to adversary failed (name=%r args=%r kwargs=%r): result=%r" % (
                key, args, kwargs, res)
            return res["content"]

        return handler

    def terminate(self):
        # Return stdout after terminating the program
        self.channel = grpc.insecure_channel(
            'unix:///var/run/cryptomato/sandbox.sock')
        stub = private_api_pb2_grpc.SandboxExecStub(self.channel)
        try:
            req = private_api_pb2.TerminateRequest(id=self.process)
            return stub.Terminate(req).output
        except:
            import traceback
            traceback.print_exc()
            return ""

    def get_target(self, key):
        return self._wrapper(key)

    def __del__(self):
        self.terminate()
