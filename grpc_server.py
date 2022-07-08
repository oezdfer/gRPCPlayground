#! /usr/bin/python3

from concurrent import futures
import sys
import time
import logging
import argparse
from xmlrpc.client import Boolean

import grpc
import order_pb2
import order_pb2_grpc


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

# A common Logger
logger = logging.getLogger('gRPC_playground')


"""
Order Receiver class
"""
class Greeter(order_pb2_grpc.OrderService):

    def AddOrder(self, order):
        logger.debug("Order received with {}".format(order))
        return order_pb2.OrderReply(result=True)


def serve( server_address=None, use_tsl=None ):

    logger.info("gRCP Server is started to serve ...")

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

    if server_address:
        server.add_secure_port(server_address + ':' + str(port), credentials)
    else:
        server.add_secure_port('[::]:' + str(port), credentials)

    logger.info("Start listening {}:{}".format(server_address, port))
    
    #server.add_secure_port('[::]:' + str(port), credentials)
    #server.add_insecure_port('[::]:50051')
    
    #logger.debug( server.__repr__ ) 
    server.start()

    server.wait_for_termination()


"""
Main
"""
if __name__ == '__main__':

    p = argparse.ArgumentParser('A python implementation of gRPC server')

    p.add_argument('-l', '--localhost', metavar='localhost',
        help='whether the localhost is used for the gRPC connection test.')
    p.add_argument('-s', '--server-address', metavar='server_address', dest='server_address',
        help='server host is used for the gRPC connection test.')
    p.add_argument('-t', '--use-tsl', metavar='tsl', dest='use_tsl',
        help='whether a remote host uses a TSL gRPC connection.')
    p.add_argument('-v', '--verbose', type=Boolean, dest='verbose', action='store', default=False,
        help='Verbose mode for logging')               

    args = p.parse_args()

    if args.verbose:
      logger.setLevel(logging.DEBUG)

    logger.info("gRCP Server is started to run ...")
    logger.debug("Arguments {} ".format(args))

    if args.server_address:
         logger.info("Remote host {}".format(args.server_address))

    if args.use_tsl:
         logger.info("Use TSL host {}".format(args.use_tsl))

    while True:
        try:

            # take start time timestamp
            start_time = time.perf_counter()

            logger.debug("Serve with server address {}".format(args.server_address))
            serve(args.server_address, args.use_tsl)

        except KeyboardInterrupt:

            # elapsed time calculation
            print('Elapsed time {:0.4f} in seconds'.format(time.perf_counter() - start_time))
            exit()

        finally:
            print('Finally')
            exit()