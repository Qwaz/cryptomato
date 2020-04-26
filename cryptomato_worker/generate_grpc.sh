#!/bin/sh
/usr/bin/env python3 -m grpc_tools.protoc -I./protos --python_out=./exposed_lib --grpc_python_out=./exposed_lib ./protos/api.proto
/usr/bin/env python3 -m grpc_tools.protoc -I./protos --python_out=./protos --grpc_python_out=./protos ./protos/private_api.proto
ln -sf ../exposed_lib/api_pb2.py protos
ln -sf ../exposed_lib/api_pb2_grpc.py protos
