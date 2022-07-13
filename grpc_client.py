#! /usr/bin/python3

from __future__ import print_function

import time
import logging
import argparse
from xmlrpc.client import Boolean

import grpc
import order_pb2
import order_pb2_grpc

from grpc_interceptor import ClientCallDetails, ClientInterceptor

class DataClientInterceptor(ClientInterceptor):

    def intercept(
        self,
        method,
        request_or_iterator,
        call_details: grpc.ClientCallDetails,
    ):
        """
        Args:
            method: A function that proceeds with the invocation by executing the next
                interceptor in the chain or invoking the actual RPC on the underlying
                channel.
            request_or_iterator: RPC request message or iterator of request messages
                for streaming requests.
            call_details: Describes an RPC to be invoked.

        Returns:
            The type of the return should match the type of the return value received
            by calling `method`. This is an object that is both a
        """
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [("authorization", "Bearer mysecrettoken")],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request_or_iterator, new_details)


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

# A common Logger
logger = logging.getLogger('gRPC_playground')

""" 
Run method for the client 
"""
def run(count, remotehost=None, port=None):
    
    """
    :param count Number of transations / messages to be sent to the gRPC server
    :param remotehost Server, i,e., gRPC server to be connected in case of a remore server is configured
    :param port Port number to be used
    """
    # .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs of the code.
    
    #with grpc.insecure_channel('10.112.130.203:50051') as channel:

    logger.debug("Passed count {}".format(count))

    if port is not None:
        server_port = port
        logger.debug("Passed port {}".format(port))
    
    server_host = 'localhost'

    server_port = 50051

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

    interceptors = [DataClientInterceptor()]
    with grpc.secure_channel(server_host + ':' + str(server_port), credentials) as channel:
        
        channel = grpc.intercept_channel(channel, *interceptors)

        # use stub for the gRCP client        
        stub = order_pb2_grpc.OrderServiceStub(channel)

        logger.debug("server host with port {}:{}".format(server_host, server_port))

        try:

            # take a timestamp for elapsed time calculation
            start_time = time.perf_counter()

            for i in range(count):
                try:
                    response = stub.AddOrder(order_pb2.Order(instrumentID=4711, price=121, quantity=10, side=True))

                    print("Result = {}".format(response.result))    
                    # Display information for each thousand transaction
                    if i % 5000 == 0:
                        logger.debug('{} transactions and elapsed time {:0.4f} in seconds'.format(i, time.perf_counter() - start_time))
                    
                except grpc.RpcError as err:
                        
                    if err.code() == grpc.StatusCode.UNAVAILABLE:
                        print("RpcError - UNAVAILABLE")
                        print(err.details())
                        exit()

            logger.info('transactions and elapsed time {:0.4f} in seconds'.format(time.perf_counter() - start_time))

        except KeyboardInterrupt:
            print("Keyboard")
            channel.unsubscribe(close)
            exit()

        except grpc.RpcError as err:
                
            if err.code() == grpc.StatusCode.UNAVAILABLE:
                print("RpcError - UNAVAILABLE")
                
            channel.close()
            exit()

        finally:
            print("Finaly, channel is closed")
            channel.close()

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
    p.add_argument('-p', '--port', metavar='port', dest='port', action='store',
        help='Port for the gRPC connection test.')
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
    run( args.count, args.remote_host, args.port )