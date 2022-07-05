#!/bin/bash

Help()
{
    # Display Help
    echo "Start the gRPC server."
    echo
    echo "Syntax: $( basename ${0} ) [-h]"
    echo "Options:"
    echo "-h, --help        Print this help."
    echo
}

PARAMS=""
while (( "$#" )); do
  case "$1" in
    -h|--help)
        Help
        exit 0
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      Help
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
  
# set positional arguments in their proper place
eval set -- "$PARAMS"

if ! command -v pipenv &> /dev/null; then
  echo "error  : Cannot find pipenv." 1>&2
  exit 3
fi

if pipenv --py 2>&1 | grep 'No virtualenv'; then
    echo "warning: No virtual environment found" 1>&2
    pipenv install
fi 

if [ ! -f order_pb2.py ]; then
    echo "warning: Generating protobuf files..." 1>&2
    pipenv run python -m run_codegen 
fi

pipenv run python -m grpc_server
 
