#!/bin/bash

set -e # Exit on error
ping -c $2 $1 # Ping host $1 for $2 times
exit 0 # Exit successfully
