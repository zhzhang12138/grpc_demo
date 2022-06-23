from concurrent import futures

import grpc

from proto import RonService_pb2
from proto import RonService_pb2_grpc


class Greeter(RonService_pb2_grpc.RonService):  # 必须继承RonService_pb2_grpc.RonService

    def SendSms(self, request, context):  # 参数固定
        print("接收：", 'Hello, %s!' % request.name)
        return RonService_pb2.SendSmsResponse(message='Hello, %s!' % request.name)


def serve():
    # 1 实例化server，grpc提供的，使用线程池跑，具备并发能力
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 2  把server和我们定义的Greeter()绑定，本质是把Greeter()注册到server中
    RonService_pb2_grpc.add_RonServiceServicer_to_server(Greeter(), server)
    # 3 启动server
    # server.add_insecure_port('[::]:50051')
    server.add_insecure_port('0.0.0.0:50051')
    # 4 启动server
    server.start()
    # 5 不让主程序结束，阻塞
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
