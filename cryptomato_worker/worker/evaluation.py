import hashlib
import json
import os

import grpc

from .challenges import *
from .protos import api_pb2
from .protos import api_pb2_grpc
from .sandbox import sandbox_py_exec

__all__ = (
    'Experiment_APIServicer',
    'Experiment_APIServiceAuthValidationInterceptor',
    'evaluate',
)

evaluation_sessions = {}


class EvaluationSession:
    def __init__(self, rpc_secret, challenge_id):
        _h = hashlib.sha3_512()
        _h.update(rpc_secret.encode('ascii'))
        self.__hashed_rpc_secret = _h.digest()
        self.__challenge_id = challenge_id
        if self.__challenge_id == 'TestChallenge1':
            self.__challenge_instance = TestChallenge1()
        else:
            raise NotImplementedError

    def is_valid_rpc_secret(self, rpc_secret):
        _h = hashlib.sha3_512()
        _h.update(rpc_secret.encode('ascii'))
        return self.__hashed_rpc_secret == _h.digest()

    def rpc(self, f, *args):
        if f.startswith('_') or not f.replace('_', '').isalnum():
            raise PermissionError

        if f in self.__challenge_instance.EXPORTS:
            return getattr(self.__challenge_instance, f)(*args)
        else:
            raise NotImplementedError

    def result(self):
        return self.__challenge_instance.result()


# noinspection PyPep8Naming
class Experiment_APIServicer(api_pb2_grpc.Experiment_APIServicer):
    @staticmethod
    def get_evaluation_session(context):
        # noinspection PyBroadException
        try:
            for metadata in context.invocation_metadata():
                if metadata.key == 'x-auth':
                    rpc_id, rpc_secret = metadata.value.split(':')
                    if evaluation_sessions[rpc_id].is_valid_rpc_secret(rpc_secret):
                        return evaluation_sessions[rpc_id]
        except Exception:
            raise PermissionError
        raise PermissionError

    def RPC(self, request, context):
        e = self.get_evaluation_session(context)
        result = e.rpc(request.f, *json.loads(request.args))
        return api_pb2.RPC_Reply(r=json.dumps(result))


# noinspection PyPep8Naming
class Experiment_APIServiceAuthValidationInterceptor(grpc.ServerInterceptor):
    def __init__(self):
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'UNAUTHENTICATED')

        self._abortion = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        # noinspection PyBroadException
        try:
            for metadata in handler_call_details.invocation_metadata:
                if metadata.key == 'x-auth':
                    rpc_id, rpc_secret = metadata.value.split(':')
                    if evaluation_sessions[rpc_id].is_valid_rpc_secret(rpc_secret):
                        return continuation(handler_call_details)
        except Exception:
            return self._abortion
        return self._abortion


def evaluate(challenge_name, code):
    rpc_id = os.urandom(16).hex()
    rpc_secret = os.urandom(32).hex()
    evaluation_sessions[rpc_id] = EvaluationSession(rpc_secret, challenge_name)
    # noinspection PyBroadException
    try:
        result = sandbox_py_exec(
            code,
            envs={'RPC_ID': rpc_id, 'RPC_SECRET': rpc_secret},
            check_output=True,
        )
        if result['type'] == 'success':
            solved, detail = evaluation_sessions[rpc_id].result()
            result = {
                'type': 'success',
                'solved': solved,
                'detail': detail,
                'user_code_output': result['output'],
            }
    except Exception as e:
        result = {'type': 'Exception', 'message': str(type(e))}
    del evaluation_sessions[rpc_id]
    return json.dumps(result)
