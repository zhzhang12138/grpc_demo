import grpc

from proto import RonService_pb2, RonService_pb2_grpc

if __name__ == "__main__":
    client = RonService_pb2_grpc.RonServiceStub(grpc.insecure_channel("0.0.0.0:50051"))
    response = client.SendSms(
        RonService_pb2.SendSmsRequest(name="Word"))
    print(response)
