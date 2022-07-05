# grcpPlayground

## Create .proto

The Protocol buffer compiler *protoc* is used to create the languange specific artifacts.

```python
python3 -m grpc_tools.protoc -I. --grpc_python_out=. --python_out=. order.proto
```
or

```python
python3 run_codegen.py
```


## gRPC Server

The gRPC server runs with a threadpool with 10 workers. 

The gRPC server receives the sent orders by the gRPC clients and replies with a Boolean that the order is received.

```python
python3 grpc_server.py --help
```

## gRPC Client

The gRPC clients sends an *Order* by using the protocol buffer to the gRPC server.  


## Multiple gRPC Clients

The *multiple* gRPC clients is used to simulate several *gRPC clients*. 

All gRPC clients is based on the same logic. They simply send an Order to the gRPC server. 

```python
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
```
