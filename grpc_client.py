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
    #-10-112-130-203
    #with grpc.insecure_channel('10.112.130.203:50051') as channel:

    #print(count)

    server_port = 50051
    server_host = 'localhost'
    ca_cert = 'server.crt'
    root_certs = open(ca_cert, 'rb').read()
    credentials = grpc.ssl_channel_credentials(root_certs)

    with grpc.secure_channel(server_host + ':' + str(server_port), credentials) as channel:
        # use stub for the gRCP client
        
        
        #channel = grpc.secure_channel(server_host + ':' + str(server_port), credentials)
        #stub = namer_pb2_grpc.NamerStub(channel)
        stub = order_pb2_grpc.OrderServiceStub(channel)

        # take a timestamp for elapsed time calculation
        #start_time = time.perf_counter()

        #print("....")

        while True:
            try:

                # take start time timestamp
                start_time = time.perf_counter()

                for i in range(count):
                    try:
                        response = stub.AddOrder(order_pb2.Order(instrumentID=4711, price=121, quantity=10, side=True))

                        print("Result = {}".format(response.result))    
                    # Display information for each thousand transaction
                    #if i % 10000 == 0:
                    #    print('{} transactions and elapsed time {:0.4f} in seconds'.format(i, time.perf_counter() - start_time))
                    except grpc.RpcError as err:
                        print(err.details())

                print('transactions and elapsed time {:0.4f} in seconds'.format(time.perf_counter() - start_time))

            except KeyboardInterrupt:
                print("Keyboard")
                channel.unsubscribe(close)
                exit()

            finally:
                print("Finaly")
                channel.close()
                exit()

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

    p.add_argument('-c', '--count', type=int, metavar='count', dest='count', help='counter')

    args = p.parse_args()

    print("Client is started to run ...")
    logging.basicConfig()

    run( args.count )