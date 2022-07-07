# Google Remote Procedure Calls (gRPC) Playground

This __gRPC__ GitHub repository is used to analyze gRPC protocol with different scenario:

* localhost latency
* server-to-server latency
* server-to-server latency with encryption

## Create .proto artifacts

The Google Protocol buffer compiler *protoc* is used to create the programming languange specific artifacts.

An *Order* of 25 - byte is used for the prototyping:

``` python
message Order {
  int64 instrumentID = 1;
  int64 price = 2;
  int64 quantity = 3;
  bool side = 4;
}
```

The corresponding python artifacts are created by using:

## Single gRPC Server

The single gRPC server runs with a threadpool with *10* workers. 

The gRPC server receives the sent orders by the gRPC clients and replies with a Boolean that the order is received.

```python
python3 grpc_server.py --help
```

## Single gRPC Client

The gRPC clients sends an *Order* by using the Google protocol buffer to the gRPC server.  

## Multiple gRPC Clients

The *multiple* gRPC clients is used to simulate several *gRPC clients*. 

All gRPC clients is based on the same logic. They simply send an Order to the gRPC server. 

### Localhost test results

The gRPC server and multiple gRPC clients run on the same local server (AWS).

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

Several runs with different number of gRPC clients:

```python
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=1000 --count=1000
Number of clients 1000 and number of order transactions 1000
transactions and elapsed time 0.2859 in seconds
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=1000 --count=10000
Number of clients 1000 and number of order transactions 10000
transactions and elapsed time 2.7039 in seconds
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=1000 --count=100000
Number of clients 1000 and number of order transactions 100000
transactions and elapsed time 27.5429 in seconds
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=10000 --count=100000
Number of clients 10000 and number of order transactions 100000
transactions and elapsed time 27.7686 in seconds
```

### Server to Server test results

The gRPC server and multiple gRPC clients run on the different server (AWS - Red Hat 7).

```python
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=1000 --count=1000
Number of clients 1000 and number of order transactions 1000
transactions and elapsed time 1.4660 in seconds
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=1000 --count=10000
Number of clients 1000 and number of order transactions 10000
transactions and elapsed time 17.7699 in seconds
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=1000 --count=100000
Number of clients 1000 and number of order transactions 100000
transactions and elapsed time 166.9796 in seconds
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=5000 --count=10000
Number of clients 5000 and number of order transactions 10000
transactions and elapsed time 14.2598 in seconds
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=10000 --count=10000
Number of clients 10000 and number of order transactions 10000
transactions and elapsed time 17.6165 in seconds
✔ 7.9.2009  cd827@ip-10-112-151-152 ~/PycharmProjects/grpc_playground $ python3 grcp_clients.py --no-of-clients=20000 --count=10000
Number of clients 20000 and number of order transactions 10000
transactions and elapsed time 17.2865 in seconds

```
