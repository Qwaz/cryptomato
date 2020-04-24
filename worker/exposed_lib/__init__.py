import json
import os
import sys

import grpc

if sys.argv[0] == '/tmp/main.py':
    sys.path.insert(0, '/tmp/cryptomato')

from . import api_pb2
from . import api_pb2_grpc

__all__ = (
    'attack',
    'lr_oracle',
    'lr_oracle_guess',
)


class AuthGateway(grpc.AuthMetadataPlugin):
    def __call__(self, context, callback):
        callback((('x-auth', os.environ['RPC_ID'] + ':' + os.environ['RPC_SECRET']),), None)


def create_client_channel(server_address):
    channel_credentials = grpc.local_channel_credentials(grpc.LocalConnectionType.UDS)
    call_credentials = grpc.metadata_call_credentials(AuthGateway())
    composite_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
    return grpc.secure_channel(server_address, composite_credentials)


rpc_channel = create_client_channel('unix:///var/run/cryptomato/api.sock')
rpc_stub = api_pb2_grpc.Experiment_APIStub(rpc_channel)


def rpc(method, *args):
    request = api_pb2.RPC_Request(f=method, args=json.dumps(args))
    response = rpc_stub.RPC(request)
    return json.loads(response.r)


def attack(attack_func):
    for _ in range(rpc('required_test_count')):
        attack_func()


def lr_oracle(m0, m1):
    return rpc('lr', m0, m1)


def lr_oracle_guess(b):
    rpc('guess_lr', b)
