# grcpPlayground

## Create .proto

python3 -m grpc_tools.protoc -I. --grpc_python_out=. --python_out=. order.proto

or

python3 run_codegen.py

## gRPC Server

python3 grpc_server.py --help

## gRPC Client

## Multiple gRPC Clients

python3 grcp_clients.py --no-of-clients=100000 --count=1000000

Number of clients 100000 and number of order transactions 1000000
0 transactions and elapsed time 0.0016 in seconds
1000 transactions and elapsed time 0.2707 in seconds
2000 transactions and elapsed time 0.5320 in seconds
3000 transactions and elapsed time 0.7929 in seconds
4000 transactions and elapsed time 1.0512 in seconds
5000 transactions and elapsed time 1.3075 in seconds
6000 transactions and elapsed time 1.5661 in seconds
7000 transactions and elapsed time 1.8335 in seconds
8000 transactions and elapsed time 2.0970 in seconds
9000 transactions and elapsed time 2.3582 in seconds
10000 transactions and elapsed time 2.6195 in seconds
