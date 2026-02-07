#!/bin/bash

set -e 

# Check systemd-resolved is running
if systemctl is-active --quiet systemd-resolved; then
    echo "systemd-resolved is running"
    echo "DNS Servers:"
    resolvectl status | grep 'DNS Servers'
else
    echo "systemd-resolved is not running"
    echo "DNS Servers:"
    cat /etc/resolv.conf | grep nameserver
fi