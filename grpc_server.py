#! /usr/bin/python3

from concurrent import futures
import sys
import time
import logging
import argparse

import grpc
import order_pb2
import order_pb2_grpc


"""
Order Receiver class
"""
class Greeter(order_pb2_grpc.OrderService):

    def AddOrder(self, order):
        return order_pb2.OrderReply(result=True)


def serve():

    print("gRCP Server is started to serve ...")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    order_pb2_grpc.add_OrderServiceServicer_to_server(Greeter, server)

    # Certificate Authority (CA) certificate handling on server
    
    port = 50051
    #server_host = 'localhost'
    keyfile = 'server.key'
    certfile = 'server.crt'
    private_key = open(keyfile, 'rb').read()
    certificate_chain = open(certfile, 'rb').read()
    credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)])

    #server.add_secure_port(server_host + ':' + str(port), credentials)
    server.add_secure_port('[::]:' + str(port), credentials)

    #print("Start listening {}:{}".format(server_host, port))
    
    #server.add_secure_port('[::]:' + str(port), credentials)
    #server.add_insecure_port('[::]:50051')
    
    print( server.__repr__ ) 
    server.start()

    server.wait_for_termination()


"""
Main
"""
if __name__ == '__main__':

    p = argparse.ArgumentParser('A python implementation of gRPC server')

    p.add_argument('-l', '--localhost', type=str, metavar='localhost',
                   help='whether the localhost is used for the gRPC connection test.')
    p.add_argument('-r', '--remote-host', type=str, metavar='remote_host', dest='remote_host',
                   help='remote host is used for the gRPC connection test.')
    p.add_argument('-t', '--tsl', metavar='tsl',
                   help='whether a remote host uses a TSL gRPC connection.')

    args = p.parse_args()

    print("gRCP Server is started to run ...")
    print("Arguments {} ".format(args))

    if args.remote_host:
         print("Remote host {}".format(args.remote_host))
    
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