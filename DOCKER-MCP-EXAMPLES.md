# Docker MCP Toolkit - Practical Examples

Real-world examples for using Docker MCP Toolkit with Gemini CLI.

## Quick Start Examples

### Example 1: Basic Container Operations

```powershell
# List all containers
gemini "List all Docker containers, including stopped ones"

# Create a simple container
gemini "Create a container named 'hello-world' using the hello-world image and run it"

# Inspect a container
gemini "Show detailed information about container 'hello-world'"

# Clean up
gemini "Remove container 'hello-world'"
```

### Example 2: Development Environment Setup

```powershell
# Create a complete dev environment
gemini "Set up a development environment:
1. Create a network called 'dev-network'
2. Create a Python 3.13 container named 'python-dev' connected to the network
3. Create a Node.js 20 container named 'node-dev' connected to the network
4. Create a shared volume 'dev-data'
5. Mount the volume to both containers"
```

### Example 3: Build and Test Workflow

```powershell
# Build, test, and clean up
gemini "Build a Docker image from Dockerfile.gemini, 
create a test container from it, run 'python --version' in the container,
show the output, then remove the container and image"
```

### Example 4: Multi-Container Application

```powershell
# Set up a web app stack
gemini "Create a web application stack:
1. Create network 'webapp-network'
2. Create a PostgreSQL container named 'db' on the network
3. Create a Python Flask container named 'api' on the network
4. Create an nginx container named 'web' on the network
5. Connect all containers to the network
6. Show the status of all containers"
```

### Example 5: CI/CD Simulation

```powershell
# Simulate CI/CD pipeline
gemini "Simulate a CI/CD pipeline:
1. Build image 'myapp:test' from Dockerfile.gemini
2. Create container 'test-runner' from the image
3. Run tests in the container (simulate with 'echo Tests passed')
4. If tests pass, tag image as 'myapp:latest'
5. Show final image list
6. Clean up test container"
```

## Advanced Examples

### Example 6: Resource Monitoring and Cleanup

```powershell
# Monitor and clean up
gemini "Show Docker resource usage:
1. List all containers with their status
2. Show disk usage
3. List all images with sizes
4. Remove all stopped containers
5. Prune unused images
6. Show final resource summary"
```

### Example 7: Isolated Testing Environment

```powershell
# Create isolated test environment
gemini "Create an isolated test environment:
1. Create network 'test-network'
2. Build test image from Dockerfile.gemini
3. Create test container with:
   - Network: test-network
   - Volume mount: current directory to /workspace
   - Environment variable: TEST_MODE=true
4. Run test command in container
5. Capture and show output
6. Clean up everything"
```

### Example 8: Service Discovery Setup

```powershell
# Set up service discovery
gemini "Create a microservices setup with service discovery:
1. Create network 'services-network'
2. Create service1 container (Python) on the network
3. Create service2 container (Node.js) on the network
4. Create service3 container (Python) on the network
5. Show how services can discover each other by container name
6. Test connectivity between services"
```

### Example 9: Backup and Restore

```powershell
# Backup container data
gemini "Backup all Docker volumes:
1. List all volumes
2. For each volume, create a backup container
3. Export volume data to a backup file
4. Verify backup files exist
5. Show backup summary"
```

### Example 10: Multi-Stage Build Optimization

```powershell
# Optimize image builds
gemini "Create an optimized multi-stage Dockerfile:
1. Stage 1: Build stage with all build tools
2. Stage 2: Runtime stage with only runtime dependencies
3. Copy artifacts from build to runtime
4. Build the optimized image
5. Compare image sizes before and after optimization"
```

## Integration Examples

### Example 11: Combine with File Operations

```powershell
# Read Dockerfile and build
gemini "Read Dockerfile.gemini, analyze it, 
suggest improvements, then build the image with the improvements"
```

### Example 12: Combine with Code Generation

```powershell
# Generate and containerize
gemini "Generate a Python Flask application,
create a Dockerfile for it, build the image,
create a container, and test it"
```

### Example 13: Combine with E2B Sandbox

```powershell
# Develop in E2B, containerize with Docker MCP
gemini "In E2B sandbox, create a Python script,
then use Docker MCP to build a Docker image for it,
create a container, and run the script"
```

### Example 14: Workflow Automation

```powershell
# Complete automation workflow
gemini "Automate the complete workflow:
1. Analyze the project structure
2. Generate appropriate Dockerfile
3. Build the image
4. Create test containers
5. Run tests
6. If tests pass, tag and prepare for deployment
7. Generate deployment instructions"
```

## Real-World Scenarios

### Scenario 1: Local Development Setup

```powershell
# Set up local dev environment
gemini "Set up my local development environment:
1. Create dev network
2. Create database container (PostgreSQL)
3. Create Redis container for caching
4. Create application container
5. Set up volumes for persistent data
6. Configure networking between services
7. Show connection strings and setup instructions"
```

### Scenario 2: Testing Multiple Python Versions

```powershell
# Test across Python versions
gemini "Test compatibility across Python versions:
1. Create containers for Python 3.10, 3.11, 3.12, 3.13
2. Run the same test script in each
3. Compare results
4. Generate compatibility report"
```

### Scenario 3: Performance Testing

```powershell
# Performance testing setup
gemini "Set up performance testing:
1. Create test network
2. Create application container with resource limits
3. Create load testing container
4. Run performance tests
5. Collect metrics
6. Generate performance report"
```

### Scenario 4: Security Scanning

```powershell
# Security scanning workflow
gemini "Set up security scanning:
1. Build application image
2. Scan image for vulnerabilities
3. Generate security report
4. If vulnerabilities found, suggest fixes
5. Rebuild with fixes if possible"
```

## Tips for Maximum Effectiveness

### 1. Be Specific

**Bad:**
```powershell
gemini "Set up Docker"
```

**Good:**
```powershell
gemini "Create a Docker network 'app-network', 
build image from Dockerfile.gemini, 
create container 'myapp' on the network, 
and start it"
```

### 2. Chain Operations

```powershell
gemini "Build image, create container, run tests, 
capture output, and clean up - all in one workflow"
```

### 3. Use Resource Limits

```powershell
gemini "Create container with CPU limit 0.5 and memory limit 512MB"
```

### 4. Always Clean Up

```powershell
gemini "After completing the task, remove all test containers and images"
```

### 5. Monitor Resources

```powershell
gemini "Before starting, show current Docker resource usage"
```

## Common Patterns

### Pattern 1: Build-Test-Deploy

```powershell
gemini "Build image 'myapp:latest', 
create test container, run tests, 
if tests pass tag as 'myapp:production', 
otherwise show error details"
```

### Pattern 2: Blue-Green Deployment

```powershell
gemini "Set up blue-green deployment:
1. Deploy 'blue' version
2. Test 'blue' version
3. If tests pass, switch traffic to 'blue'
4. Keep 'green' as backup"
```

### Pattern 3: Canary Deployment

```powershell
gemini "Set up canary deployment:
1. Deploy new version to 10% of containers
2. Monitor performance
3. Gradually increase to 100% if stable"
```

## Troubleshooting Examples

### Debug Container Issues

```powershell
gemini "Debug container 'myapp':
1. Show container logs
2. Inspect container configuration
3. Check resource usage
4. Test connectivity
5. Suggest fixes"
```

### Resolve Resource Issues

```powershell
gemini "Resolve Docker resource issues:
1. Show current resource usage
2. Identify resource-heavy containers
3. Suggest cleanup actions
4. Execute cleanup
5. Verify resource availability"
```

## Next Steps

1. Try these examples with your own projects
2. Adapt patterns to your specific needs
3. Combine with other MCP servers (GitHub, Notion)
4. Create custom workflows
5. Share your own examples!

