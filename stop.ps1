# Stop Docker Compose services
docker-compose down

# Close all terminal windows
Get-Process | Where-Object {$_.MainWindowTitle -like "Command Prompt*"} | ForEach-Object {Stop-Process -Id $_.Id}
