#!/bin/bash
set -e

dns_servers=()

if systemctl is-active --quiet systemd-resolved; then
    echo "systemd-resolved is running"
    dns_servers=($(resolvectl dns | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}'))
else
    echo "systemd-resolved is not running"
    dns_servers=($(grep nameserver /etc/resolv.conf | awk '{print $2}'))
fi

mapfile -t dns_servers < <(printf "%s\n" "${dns_servers[@]}" | sort -u)

echo "Discovered DNS servers:"
count=1
for dns in "${dns_servers[@]}"; do
    echo "$count. $dns"
    count=$((count + 1))
done

echo "Enter the number of the DNS server to test, or press Enter to test all:"
read -r choice

servers_to_test=()

if [[ -z "$choice" ]]; then
    servers_to_test=("${dns_servers[@]}")
else
    if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt "${#dns_servers[@]}" ]; then
        exit 1
    fi
    servers_to_test=("${dns_servers[$((choice-1))]}")
fi

echo ""
for server in "${servers_to_test[@]}"; do
    echo "Testing DNS server $server..."
    nslookup google.com "$server"
    echo ""
done
