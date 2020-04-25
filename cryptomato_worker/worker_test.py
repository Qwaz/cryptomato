from protos import private_api_pb2
from protos import private_api_pb2_grpc
import grpc


def test(challenge_name, code):
    with grpc.insecure_channel('unix:///var/run/cryptomato/manager.sock') as channel:
        stub = private_api_pb2_grpc.ManagerStub(channel)
        response = stub.Evaluation(private_api_pb2.EvaluationRequest(challenge_name=challenge_name, code=code))
        channel.close()
        return response.result


print('TestChallenge1', test('TestChallenge1', """
from cryptomato import *

print("HELLO")

def attack_impl():
    if lr_oracle("1234", "5678") == "4321":
        lr_oracle_guess(0)
    else:
        lr_oracle_guess(1)

attack(attack_impl)
"""))
