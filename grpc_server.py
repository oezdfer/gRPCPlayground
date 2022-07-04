#! /usr/bin/python3

from concurrent import futures
import logging

import grpc
import order_pb2
import order_pb2_grpc


class Greeter(order_pb2_grpc.OrderService):

    def AddOrder(self, order):
        return order_pb2.OrderReply(result=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(Greeter, server)
    server.add_insecure_port('[::]:50051')
    server.start()

    server.wait_for_termination()


if __name__ == '__main__':
    print("Server is started to run ...")
    logging.basicConfig()
    serve()