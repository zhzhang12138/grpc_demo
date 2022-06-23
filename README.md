---
title: 'Python使用grpc相互通信'
tags:
  - Grpc
categories:
  - Grpc
date: 2022-04-12 14:30:00
top_img: transparent
cover: https://img2.baidu.com/it/u=3558077636,741039655&fm=253&fmt=auto&app=138&f=JPEG?w=866&h=500
---

## Protobuf 介绍

Protobuf 是 Google 给出的一种通用的数据表示方式，通过 proto 文件定义的数据格式，可以一键式的生成 C++，Python，Java 等各种语言实现

protobuf经历了protobuf2和protobuf3，pb3比pb2简化了很多，目前主流的版本是pb3

![image-20220111143156845](https://picture-typora-bucket.oss-cn-shanghai.aliyuncs.com/typora/image-20220111143156845.png)

### 生成proto的python文件

```python
# 通过book.proto生成py脚本文件，
# --python_out=.        跟proto相关的python脚本，输出到当前路径
# --grpc_python_out=.   给grpc用的文件，输出到当前路径
# -I. book.proto        从当前路径下找book.proto
python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. book.proto
```

## Python使用grpc相互通信

### 目录结构

```python
-grpc  													 # 包名
  -proto                   			 # 文件夹
    -RonService.proto            # 自己定义的proto 
    -RonService_pb2.py 					 # 命令生成
    -RonService_pb2_grpc.py      # 命令生成
  -client.py               			 # rpc客户端
  -server.py              		   # rpc服务端
```

### helloworld.proto

```protobuf
syntax = "proto3";

// 包名
package RonService;

// 请求参数对象
message SendSmsRequest {
  string name = 1;
}

// 返回参数对象
message SendSmsResponse {
  string message = 1;
}

// 对外暴露的服务
service RonService {
  // 对外暴露的函数名，参数和返回值
  rpc SendSms (SendSmsRequest) returns (SendSmsResponse) {};
}

```

### 执行脚本，生成py文件

```python
python3 -m grpc_tools.protoc -I<目标路径目录> --python_out=. --grpc_python_out=<目标文件所在目录路径> <目标文件data.proto>

# 切换到proto文件夹下执行
python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto
# 会生成helloworld_pb2_grpc.py    helloworld_pb2.py
```

### server.py

```python
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
```

### client.py

```python
import grpc

from proto import RonService_pb2, RonService_pb2_grpc

if __name__ == "__main__":
    client = RonService_pb2_grpc.RonServiceStub(grpc.insecure_channel("0.0.0.0:50051"))
    response = client.SendSms(
        RonService_pb2.SendSmsRequest(name="Word"))
    print(response)
```

### 注意

```python
# 生成的helloworld_pb2_grpc.py 因为引用了helloworld_pb2.py，包导入会有问题
# 需要修改第五行为
from proto import RonService_pb2 as RonService__pb2
```

### 运行服务端，运行客户端

```python
python3 server.py # 运行服务端

python3 client.py # 运行客户端
```

