# Get DNS servers

$dns_servers = Get-DnsClientServerAddress | Where-Object {$_.ServerAddresses} | ForEach-Object {$_.ServerAddresses}

# Print DNS servers
Write-Host "Discovered DNS servers:"
$count = 1
foreach ($dns in $dns_servers) {
    Write-Host "$count. $dns"
    $count++
}

# Ask user which DNS server to use
Write-Host "Enter the number of the DNS server to test, or press Enter to test all:"
$choice = Read-Host

# Determine which servers to test
$servers_to_test = @()
if ([string]::IsNullOrEmpty($choice)) {
    # No choice given → test all servers
    $servers_to_test = $dns_servers
} else {
    # User picked a number → validate input
    if ($choice -match '^\d+$' -and $choice -ge 1 -and $choice -le $dns_servers.Count) {
        $servers_to_test += $dns_servers[$choice - 1]
    } else {
        Write-Host "Invalid choice. Exiting."
        exit 1
    }
}

# Test each DNS server with nslookup
Write-Host ""
foreach ($server in $servers_to_test) {
    Write-Host "Testing DNS server $server..."
    nslookup google.com $server
    Write-Host ""
}