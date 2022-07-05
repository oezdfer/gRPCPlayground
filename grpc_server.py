#! /usr/bin/python3
import sys
from concurrent import futures
import time
import logging
import argparse

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

    p = argparse.ArgumentParser('A python implementation of gRPC client')

    p.add_argument('-l', '--localhost', metavar='localhost', nargs=1,
                   help='whether the localhost is used for the gRPC connection test.')
    p.add_argument('-t', '--tsl', metavar='tsl', nargs=1,
                   help='whether a remote host uses a TSL gRPC connection.')

    arg = p.parse_args()

    print("gRCP Server is started to run ...")

    logging.basicConfig()

    while True:
        try:

            # take start time timestamp
            start_time = time.perf_counter()

            serve()

        except KeyboardInterrupt:

            # elapsed time calculation
            print('Elapsed time {:0.4f} in seconds'.format(time.perf_counter() - start_time))

            exit()

        finally:

            exit()