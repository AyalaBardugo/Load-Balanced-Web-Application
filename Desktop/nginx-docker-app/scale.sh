#!/bin/bash

# Check if the first parameter (number of replicas) is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <number_of_replicas>"
    exit 1
fi

# Scale the app service to the specified number of replicas
docker compose up -d --scale app=$1

# Print a success message
echo "Scaled app service to $1 replicas"
