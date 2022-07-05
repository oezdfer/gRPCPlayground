#!/usr/bin/env python3
import pyperf
import grpc_client as client

def run():
    client.run(10)

runner = pyperf.Runner()
runner.bench_func("Ferudun's grpc", run)
