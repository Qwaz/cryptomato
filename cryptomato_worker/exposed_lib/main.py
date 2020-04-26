import collections
import importlib.util
import json
import os
import struct

import grpc
from cryptomato import api_pb2
from cryptomato import api_pb2_grpc


class AuthGateway(grpc.AuthMetadataPlugin):
    def __call__(self, context, callback):
        callback(
            (('x-auth', os.environ['RPC_ID'] + ':' + os.environ['RPC_SECRET']),), None)


def create_client_channel(server_address):
    channel_credentials = grpc.local_channel_credentials(
        grpc.LocalConnectionType.UDS)
    call_credentials = grpc.metadata_call_credentials(AuthGateway())
    composite_credentials = grpc.composite_channel_credentials(
        channel_credentials, call_credentials)
    return grpc.secure_channel(server_address, composite_credentials)


rpc_channel = create_client_channel('unix:///var/run/cryptomato/api.sock')
rpc_stub = api_pb2_grpc.Experiment_APIStub(rpc_channel)


def rpc(method, *args):
    request = api_pb2.RPC_Request(f=method, args=json.dumps(args))
    response = rpc_stub.RPC(request)
    return json.loads(response.r)


class_cache = {}


def namedtuple_cached(name, keys):
    keys = tuple(keys)
    if (name, keys) not in class_cache:
        class_cache[name, keys] = collections.namedtuple(name, keys)
    return class_cache[name, keys]


def deserialize_arg(arg):
    if arg["type"] == "primitive":
        value = arg["value"]
        if isinstance(value, dict):
            return {key: deserialize_arg(v) for key, v in value.items()}
        if isinstance(value, list):
            return [deserialize_arg(_) for _ in value]
        return value
    if arg["type"] == "class":
        return namedtuple_cached(arg["name"], arg["value"].keys())(
            **{k: deserialize_arg(v) for k, v in arg["value"].items()})
    if arg["type"] == "rpc":
        return lambda *args: rpc(arg["id"], *args)


def deserialize_args(args, kwargs):
    return [deserialize_arg(_) for _ in args], {key: deserialize_arg(value) for key, value in kwargs.items()}


# Hardcoded in sandbox.py
PATH = '/tmp/user.py'


def serve_requests():
    # Attach adversary
    spec = importlib.util.spec_from_file_location("_adversary", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    ipc_in = os.fdopen(int(os.getenv("IPC_IN")), "w+b", 0)
    ipc_out = os.fdopen(int(os.getenv("IPC_OUT")), "w+b", 0)

    while True:
        length, = struct.unpack("<L", ipc_in.read(4))
        data = b''
        keep = True
        while len(data) < length:
            chunk = ipc_in.read(length - len(data))
            if not chunk:
                keep = False
                break
            data += chunk
        if not keep:
            break

        obj = json.loads(data)
        if obj.get("exit"):
            break

        args, kwargs = deserialize_args(obj["args"], obj["kwargs"])
        res = getattr(module, obj["name"])(*args, **kwargs)
        payload = json.dumps(res).encode()
        ipc_out.write(struct.pack("<L", len(payload)) + payload)


# main
if __name__ == '__main__':
    serve_requests()
