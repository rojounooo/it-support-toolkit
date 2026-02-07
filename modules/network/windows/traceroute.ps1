# Check if host is provided
if (-not $host) {
    Write-Host "Please provide a host"
    exit 1
}

# Run traceroute
Test-NetConnection -ComputerName $host -TraceRoute