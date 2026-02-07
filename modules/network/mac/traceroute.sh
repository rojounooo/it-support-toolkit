#!/bin/bash

set -e

# Get host from arguments
host=$1

# Check if host is provided
if [ -z "$host" ]; then
    echo "Please provide a host"
    exit 1
fi

# Run traceroute
traceroute $host