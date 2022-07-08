#! /usr/bin/python3

from __future__ import print_function

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
Run method for the client 
"""
def run( count, remotehost=None):
    
    """
    :param count Number of transations / messages to be sent to the gRPC server
    """
    # .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs of the code.
    
    #with grpc.insecure_channel('10.112.130.203:50051') as channel:

    logger.debug("Passed count {}".format(count))

    server_port = 50051

    server_host = 'localhost'

    if remotehost is not None:
        server_host=remotehost
        logger.debug("Passed remotehost {}".format(remotehost))

    """
    Certicate is created by using ssl
    openssl genrsa -out server.key 2048
    """
    ca_cert = 'server.crt'
    root_certs = open(ca_cert, 'rb').read()
    credentials = grpc.ssl_channel_credentials(root_certs)

    with grpc.secure_channel(server_host + ':' + str(server_port), credentials) as channel:
        
        # use stub for the gRCP client        
        stub = order_pb2_grpc.OrderServiceStub(channel)

        logger.debug("server_host{}':' + server_port{}".format(server_host, server_port))

        while True:
            try:

                # take a timestamp for elapsed time calculation
                start_time = time.perf_counter()

                for i in range(count):
                    try:
                        response = stub.AddOrder(order_pb2.Order(instrumentID=4711, price=121, quantity=10, side=True))

                        #print("Result = {}".format(response.result))    
                        # Display information for each thousand transaction
                        if i % 5000 == 0:
                            logger.debug('{} transactions and elapsed time {:0.4f} in seconds'.format(i, time.perf_counter() - start_time))
                    
                    except grpc.RpcError as err:
                        print(err.details())

                logger.info('transactions and elapsed time {:0.4f} in seconds'.format(time.perf_counter() - start_time))

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


"""
Main
"""

if __name__ == '__main__':

    p = argparse.ArgumentParser('A python implementation of gRPC client')

    p.add_argument('-l', '--local-host', metavar='localhost', dest='localhost', action='store', 
        help='whether the localhost is used for the gRPC connection test.')
    p.add_argument('-r', '--remote-host', metavar='remotehost', dest='remote_host', action='store',
        help='whether a remote host is used for the gRPC connection test.')
    p.add_argument('-c', '--count', type=int, metavar='count', dest='count',
        help='counter')
    p.add_argument('-v', '--verbose', type=Boolean, dest='verbose', action='store', default=False,
        help='Verbose mode for logging')

    # parse to get the arguments
    args = p.parse_args()

    if args.verbose:
      logger.setLevel(logging.DEBUG)

    logger.debug("Arguments {} ".format(args))
    logger.info("Client is started to run ...")
   
    # Run Baby run ...
    run( args.count, args.remotehost )