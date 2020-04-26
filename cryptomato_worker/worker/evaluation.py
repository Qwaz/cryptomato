import hashlib
import importlib.util
import json
import os
import sys
import traceback

import grpc

from . import BASEPATH
from .protos import api_pb2
from .protos import api_pb2_grpc
from .wrapper import RPCWrapper

__all__ = (
    'Experiment_APIServicer',
    'Experiment_APIServiceAuthValidationInterceptor',
    'evaluate',
)

evaluation_sessions = {}
sys.path.append("/cryptomato_worker/")


class EvaluationSession:
    def __init__(self, rpc_secret, challenge_id):
        _h = hashlib.sha3_512()
        _h.update(rpc_secret.encode('ascii'))
        self.__hashed_rpc_secret = _h.digest()
        self.__challenge_id = challenge_id

        # Run tester
        self.__challenge_instance = self._import_path(
            os.path.join(BASEPATH, "challenges", challenge_id + '.test.py'))
        self.wrapper = None

    @staticmethod
    def _import_path(path):
        spec = importlib.util.spec_from_file_location("_tester", path)
        tester = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tester)
        return tester

    def exec(self, code, rpc_id, rpc_secret):
        self.wrapper = RPCWrapper(code, {'RPC_ID': rpc_id, 'RPC_SECRET': rpc_secret, 'PYTHONUNBUFFERED': '1'})
        result = self.__challenge_instance.test(self.wrapper)
        return {
            'type': 'success',
            'solved': result['status'] == 'success',
            'detail': result,
            'user_code_output': json.dumps(result),
        }

    def is_valid_rpc_secret(self, rpc_secret):
        _h = hashlib.sha3_512()
        _h.update(rpc_secret.encode('ascii'))
        return self.__hashed_rpc_secret == _h.digest()

    def rpc(self, f, *args, **kwargs):
        f = self.wrapper.query_obj(f)
        if f:
            return f(*args, **kwargs)
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
    try:
        evaluation_sessions[rpc_id] = EvaluationSession(rpc_secret, challenge_name)
    except Exception as e:
        return json.dumps({
            'type': 'Exception',
            'message': 'Tester load exception: ' + traceback.format_exc()
        })

    # noinspection PyBroadException
    try:
        result = evaluation_sessions[rpc_id].exec(code, rpc_id, rpc_secret)
    except Exception as e:
        result = {'type': 'Exception', 'message': traceback.format_exc()}

    del evaluation_sessions[rpc_id]
    return json.dumps(result)
