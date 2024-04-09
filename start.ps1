# Start Docker Compose services
docker-compose up --build -d

# Get a list of running containers
$containers = docker ps --format "{{.Names}}"

# Loop through each container and attach to it in a new terminal window
foreach ($container in $containers) {
    Start-Process docker -ArgumentList "attach $container"
}
