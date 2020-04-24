#!/bin/sh
./venv/bin/python -m grpc_tools.protoc -I./protos --python_out=./exposed_lib --grpc_python_out=./exposed_lib ./protos/api.proto
./venv/bin/python -m grpc_tools.protoc -I./protos --python_out=./protos --grpc_python_out=./protos ./protos/private_api.proto
ln -s ../exposed_lib/api_pb2.py protos
ln -s ../exposed_lib/api_pb2_grpc.py protos
