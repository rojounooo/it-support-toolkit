#!/bin/bash

set -e

# Step 1: Detect DNS servers
dns_servers=()

if systemctl is-active --quiet systemd-resolved; then
    echo "systemd-resolved is running"
    # Extract all DNS server IPs into an array
    dns_servers=($(resolvectl status | grep 'DNS Servers' | awk '{for(i=2;i<=NF;i++) print $i}'))
else
    echo "systemd-resolved is not running"
    # Fallback to /etc/resolv.conf
    dns_servers=($(grep nameserver /etc/resolv.conf | awk '{print $2}'))
fi

# Step 2: Print all discovered DNS servers
echo "Discovered DNS servers:"
count=1
for dns in "${dns_servers[@]}"; do
    echo "$count. $dns"
    count=$((count + 1))
done

# Step 3: Ask user which DNS server to use (optional)
echo "Enter the number of the DNS server to test, or press Enter to test all:"
read choice

# Step 4: Determine which servers to test
servers_to_test=()
if [[ -z "$choice" ]]; then
    # No choice given → test all servers
    servers_to_test=("${dns_servers[@]}")
else
    # User picked a number → validate input
    if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt "${#dns_servers[@]}" ]; then
        echo "Invalid choice. Exiting."
        exit 1
    fi
    servers_to_test=("${dns_servers[$((choice-1))]}")
fi

# Step 5: Test each DNS server with nslookup
echo ""
for server in "${servers_to_test[@]}"; do
    echo "Testing DNS server $server..."
    nslookup google.com "$server"
    echo ""
done
