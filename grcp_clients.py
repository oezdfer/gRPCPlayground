#! /usr/bin/python3

from multiprocessing import Process

import grpc_client as client
import argparse

"""
Multiple gRCP clients
"""

if __name__ == "__main__":

    # Options arguments
    p = argparse.ArgumentParser('A python implementation of gRPC client')

    p.add_argument('-l', '--no-of-clients', type=int, dest='client_count', action='store', help='Number of clients')
    p.add_argument('-c', '--count', type=int, dest='count', action='store', help='counter')

    # parse to get the arguments
    args = p.parse_args()

    print("Arguments {} ".format(args))
    
    # declare a dictionary for the gRCP clients
    processes = {}

    print("Number of clients {} and number of order transactions {}".format(args.client_count, args.count))

    # To run each gRCP client
    for i in range(args.client_count):
        #processes[i] = Process(target=client.run(args.count))
        processes[i] = Process(target=client.run(args.count))
    # start all gRCP clients
    for i in range(args.client_count):
        processes[i].start()



