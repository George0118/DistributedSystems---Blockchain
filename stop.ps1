# Stop Docker Compose services
docker-compose down --rmi all

# Close all terminal windows
Get-Process | Where-Object {$_.MainWindowTitle -like "Command Prompt*"} | ForEach-Object {Stop-Process -Id $_.Id}
