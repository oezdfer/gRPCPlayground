#! /usr/bin/python3

from __future__ import print_function

import time
import logging
import argparse

import grpc
import order_pb2
import order_pb2_grpc


def run(count):

    # .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs of the code.
    with grpc.insecure_channel('localhost:50051') as channel:

        # use stub for the gRCP client
        stub = order_pb2_grpc.OrderServiceStub(channel)

        # take a timestamp for elapsed time calculation
        #start_time = time.perf_counter()

        while True:
            try:

                # take start time timestamp
                start_time = time.perf_counter()

                for i in range(count):
                    response = stub.AddOrder(order_pb2.Order(instrumentID=4711, price=121, quantity=10, side=True))

                    # Display information for each thousand transaction
                    if i % 1000 == 0:
                        print('{} transactions and elapsed time {:0.4f} in seconds'.format(i, time.perf_counter() - start_time))

            except KeyboardInterrupt:
                channel.unsubscribe( close )
                exit()

            finally:
                channel.close()

    # elapsed time calculation
    print('Elapsed time {:0.4f} in seconds'.format(time.perf_counter() - start_time))


def close(channel):
    channel.close()


if __name__ == '__main__':

    p = argparse.ArgumentParser('A python implementation of gRPC client')

    p.add_argument('-l', '--local-host', metavar='localhost', nargs=1,
                   help='whether the localhost is used for the gRPC connection test.')
    p.add_argument('-r', '--remote-host', metavar='remotehost', nargs=1,
                   help='whether a remote host is used for the gRPC connection test.')

    p.add_argument('-c', '--count', metavar='count', nargs=1, dest='count', help='counter')

    args = p.parse_args()

    print("Client is started to run ...")
    logging.basicConfig()

    run( args.count )