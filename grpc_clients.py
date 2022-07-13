#! /usr/bin/python3

from multiprocessing import Process

import grpc_client as client
import logging
import argparse

"""
Main - Multiple gRCP clients

A Process is started for each gRPC client to simulate multiple sending clients.
"""

if __name__ == "__main__":

    # Options arguments
    p = argparse.ArgumentParser('A python implementation of gRPC multiple clients')

    p.add_argument('-l', '--no-of-clients', type=int, dest='client_count', action='store', required=True, 
        help='Number of clients')
    p.add_argument('-c', '--count', type=int, dest='count', action='store', default=5,
        help='counter for the sending orders')
    p.add_argument('-v', '--verbose', action='store_true',
        help='Verbose mode for logging')    
    
    # parse to get the arguments
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    # A common Logger
    logger = logging.getLogger('gRPC_playground')

    if args.verbose:
      logger.setLevel(logging.DEBUG)

    logger.debug("Arguments are {} ".format(args))
    
    # declare a dictionary for the gRCP clients
    processes = {}

    logger.info("Number of clients {} and number of order transactions {}".format(args.client_count, args.count))

    # Set up Processes to be able to run each gRCP client
    for i in range(args.client_count):
        processes[i] = Process(target=client.run(args.count))
    
    # start all gRCP clients
    for i in range(args.client_count):
        processes[i].start()
