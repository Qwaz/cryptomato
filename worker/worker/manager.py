from .evaluation import evaluate
from .protos import private_api_pb2
from .protos import private_api_pb2_grpc

__all__ = (
    'ManagerServicer',
)


# noinspection PyPep8Naming
class ManagerServicer(private_api_pb2_grpc.ManagerServicer):
    def Evaluation(self, request, context):
        return private_api_pb2.EvaluationReply(result=evaluate(request.challenge_name, request.code))
