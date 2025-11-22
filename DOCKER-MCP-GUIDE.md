# Docker MCP Toolkit - Complete Usage Guide

Comprehensive guide to maximizing Docker MCP Toolkit usage across local, Docker containers, and EC2 sandbox environments.

## Table of Contents

1. [Overview](#overview)
2. [Docker MCP Toolkit Components](#docker-mcp-toolkit-components)
3. [Available Tools & Capabilities](#available-tools--capabilities)
4. [Setup & Configuration](#setup--configuration)
5. [Usage Examples](#usage-examples)
6. [Advanced Patterns](#advanced-patterns)
7. [Best Practices](#best-practices)
8. [Integration with Gemini CLI](#integration-with-gemini-cli)
9. [Troubleshooting](#troubleshooting)

## Overview

The Docker MCP Toolkit provides a comprehensive set of tools for managing Docker containers, images, volumes, networks, and more through the Model Context Protocol (MCP). This allows AI agents like Gemini CLI to interact with Docker directly, enabling powerful automation and orchestration capabilities.

### Key Benefits

- **Container Management**: Create, start, stop, and manage containers
- **Image Operations**: Build, pull, push, and manage Docker images
- **Volume Management**: Create and manage persistent storage
- **Network Operations**: Configure and manage Docker networks
- **Compose Support**: Work with docker-compose files
- **Resource Management**: Monitor and limit resource usage
- **Security**: Isolated execution with resource limits

## Docker MCP Toolkit Components

### 1. MCP Gateway

The MCP Gateway acts as a centralized proxy between clients (like Gemini CLI) and MCP servers. It manages:
- Configuration
- Credentials
- Access control
- Server lifecycle
- Routing

**Start the Gateway:**
```powershell
docker mcp gateway run
```

### 2. MCP Catalog

A curated collection of 200+ verified MCP servers including:
- Development tools (GitHub, GitLab)
- Cloud services (AWS, Azure, GCP)
- Data tools (Elastic, MongoDB)
- Monitoring (New Relic, Datadog)
- And many more

**Browse Catalog:**
- Docker Desktop UI: Navigate to MCP section
- CLI: Use dynamic MCP discovery

### 3. MCP Toolkit

Integrated into Docker Desktop, provides:
- Graphical interface for server management
- Secure credential storage
- OAuth authentication
- Resource limits (1 CPU, 2GB RAM per tool)

## Available Tools & Capabilities

### Container Management Tools

**Create Container:**
```powershell
# Via Gemini CLI
gemini "Create a Docker container running Python 3.13"

# The MCP server provides tools like:
# - docker_container_create
# - docker_container_start
# - docker_container_stop
# - docker_container_remove
# - docker_container_list
# - docker_container_inspect
# - docker_container_logs
# - docker_container_exec
```

**Example Commands:**
```powershell
gemini "List all running Docker containers"
gemini "Create a container named 'test-python' with Python 3.13"
gemini "Start the container named 'test-python'"
gemini "Get logs from container 'test-python'"
gemini "Execute a command in container 'test-python': python --version"
gemini "Stop and remove container 'test-python'"
```

### Image Management Tools

**Build and Manage Images:**
```powershell
gemini "Build a Docker image from Dockerfile.gemini"
gemini "List all Docker images"
gemini "Pull the latest Python image"
gemini "Tag image 'gemini-cli' as 'gemini-cli:v1.0'"
gemini "Push image 'gemini-cli:v1.0' to registry"
gemini "Remove unused images"
```

**Available Tools:**
- `docker_image_build` - Build images from Dockerfile
- `docker_image_pull` - Pull images from registry
- `docker_image_push` - Push images to registry
- `docker_image_list` - List images
- `docker_image_inspect` - Inspect image details
- `docker_image_remove` - Remove images
- `docker_image_tag` - Tag images

### Volume Management Tools

**Manage Persistent Storage:**
```powershell
gemini "Create a Docker volume named 'project-data'"
gemini "List all Docker volumes"
gemini "Inspect volume 'project-data'"
gemini "Remove volume 'project-data'"
gemini "Create a volume with specific driver"
```

**Available Tools:**
- `docker_volume_create` - Create volumes
- `docker_volume_list` - List volumes
- `docker_volume_inspect` - Inspect volumes
- `docker_volume_remove` - Remove volumes
- `docker_volume_prune` - Remove unused volumes

### Network Management Tools

**Configure Networks:**
```powershell
gemini "Create a Docker network named 'app-network'"
gemini "List all Docker networks"
gemini "Connect container 'test-python' to network 'app-network'"
gemini "Disconnect container from network"
gemini "Remove network 'app-network'"
```

**Available Tools:**
- `docker_network_create` - Create networks
- `docker_network_list` - List networks
- `docker_network_inspect` - Inspect networks
- `docker_network_connect` - Connect containers
- `docker_network_disconnect` - Disconnect containers
- `docker_network_remove` - Remove networks

### Docker Compose Tools

**Work with Compose Files:**
```powershell
gemini "Start services defined in docker-compose.yml"
gemini "Stop services in docker-compose.yml"
gemini "Build images for docker-compose.yml"
gemini "View logs from docker-compose services"
gemini "Scale a service to 3 instances"
```

**Available Tools:**
- `docker_compose_up` - Start services
- `docker_compose_down` - Stop services
- `docker_compose_build` - Build images
- `docker_compose_logs` - View logs
- `docker_compose_ps` - List services
- `docker_compose_scale` - Scale services

### System & Monitoring Tools

**System Information:**
```powershell
gemini "Show Docker system information"
gemini "Show Docker disk usage"
gemini "Show Docker version"
gemini "Prune unused Docker resources"
```

**Available Tools:**
- `docker_system_info` - System information
- `docker_system_df` - Disk usage
- `docker_system_prune` - Clean up resources
- `docker_version` - Version information

## Setup & Configuration

### 1. Install Docker MCP Gateway

The gateway is included with Docker Desktop. If not available:

```powershell
# Check if available
docker mcp gateway --help

# Start gateway (runs in background)
docker mcp gateway run
```

### 2. Configure Gemini CLI

**Check Current Configuration:**
```powershell
gemini mcp list
```

**Expected Output:**
```
Configured MCP servers:
  ✓ MCP_DOCKER: docker mcp gateway run (stdio) - Connected
```

**If Not Configured:**
```powershell
# The Docker MCP server should auto-configure with Docker Desktop
# If needed, manually add:
gemini mcp add docker --command "docker mcp gateway run"
```

### 3. Verify Connection

**Test Docker MCP:**
```powershell
# Simple test
gemini "List all Docker containers"

# Should return container list or empty list if none running
```

## Usage Examples

### Example 1: Development Environment Setup

**Create a complete development environment:**
```powershell
gemini "Create a development environment with:
1. A Python 3.13 container named 'dev-python'
2. A Node.js 20 container named 'dev-node'
3. A shared network 'dev-network'
4. A volume 'dev-data' mounted to both containers"
```

### Example 2: Build and Test Workflow

**Automated build and test:**
```powershell
gemini "Build the Docker image from Dockerfile.gemini, 
then create a test container, run tests, and clean up"
```

### Example 3: Multi-Container Application

**Set up a multi-container app:**
```powershell
gemini "Create a web application with:
1. A frontend container (nginx)
2. A backend container (Python Flask)
3. A database container (PostgreSQL)
4. Connect them via a Docker network
5. Set up volumes for persistent data"
```

### Example 4: CI/CD Pipeline Simulation

**Simulate CI/CD:**
```powershell
gemini "Simulate a CI/CD pipeline:
1. Build the application image
2. Run tests in a test container
3. Tag the image if tests pass
4. Push to registry (if configured)
5. Deploy to a staging container"
```

### Example 5: Resource Management

**Monitor and manage resources:**
```powershell
gemini "Show Docker resource usage and clean up:
1. List all containers and their resource usage
2. Show disk usage
3. Remove stopped containers
4. Prune unused images and volumes"
```

## Advanced Patterns

### Pattern 1: Dynamic Container Orchestration

**Create containers on-demand:**
```powershell
gemini "For each Python file in this directory, 
create a container to test it, run it, capture output, 
then clean up the container"
```

### Pattern 2: Isolated Testing Environments

**Test in isolated environments:**
```powershell
gemini "Create an isolated test environment:
1. Build test image
2. Create test container with volume mount
3. Run test suite
4. Capture results
5. Clean up"
```

### Pattern 3: Multi-Stage Builds

**Optimize image builds:**
```powershell
gemini "Create a multi-stage Dockerfile that:
1. Builds the application in a builder stage
2. Copies artifacts to a minimal runtime stage
3. Builds the optimized image"
```

### Pattern 4: Service Discovery

**Set up service discovery:**
```powershell
gemini "Create a microservices setup:
1. Create a custom network
2. Deploy multiple services
3. Configure them to discover each other by name
4. Set up health checks"
```

### Pattern 5: Backup and Restore

**Backup container data:**
```powershell
gemini "Backup all container data:
1. List all volumes
2. Create backups of each volume
3. Store backups with timestamps
4. Verify backup integrity"
```

## Best Practices

### 1. Resource Management

**Set Resource Limits:**
```powershell
# Docker MCP tools automatically enforce limits (1 CPU, 2GB RAM)
# But you can also specify limits when creating containers:
gemini "Create a container with CPU limit of 0.5 and memory limit of 512MB"
```

### 2. Security

**Use Read-Only Containers:**
```powershell
gemini "Create a read-only container for running untrusted code"
```

**Network Isolation:**
```powershell
gemini "Create containers in isolated networks for security"
```

### 3. Cleanup

**Always Clean Up:**
```powershell
gemini "After completing the task, remove all test containers and images"
```

**Automated Cleanup:**
```powershell
gemini "Set up a cleanup routine that removes containers older than 24 hours"
```

### 4. Monitoring

**Monitor Resource Usage:**
```powershell
gemini "Show current Docker resource usage and identify resource-heavy containers"
```

### 5. Version Control

**Tag Images Properly:**
```powershell
gemini "Tag images with version numbers and commit hashes for traceability"
```

## Integration with Gemini CLI

### Basic Integration

**Direct Commands:**
```powershell
# Gemini CLI automatically uses Docker MCP when available
gemini "List Docker containers"
```

### Advanced Integration

**Combine with Other Tools:**
```powershell
# Combine Docker MCP with file operations
gemini "Read Dockerfile.gemini, build the image, then run a container"

# Combine with code generation
gemini "Generate a Dockerfile for a Python app, build it, and test it"

# Combine with E2B sandbox
gemini "Use E2B sandbox to create a script, then Docker MCP to containerize it"
```

### Workflow Integration

**Complete Development Workflow:**
```powershell
# 1. Plan
gemini "Design a containerized microservice architecture"

# 2. Generate
gemini "Generate Dockerfiles and docker-compose.yml for the architecture"

# 3. Build
gemini "Build all Docker images"

# 4. Deploy
gemini "Start all services using docker-compose"

# 5. Test
gemini "Run integration tests against the deployed services"

# 6. Monitor
gemini "Monitor service health and logs"
```

## Maximizing Usage Across Environments

### Local Development

**Quick Iterations:**
```powershell
# Fast container creation for testing
gemini "Create a quick test container, run command, show output, remove"
```

### Docker Containers

**Consistent Environments:**
```powershell
# Use Docker MCP to manage containers from within containers
gemini "From within this container, manage other Docker containers"
```

### EC2 Sandbox

**Production-Like Setup:**
```powershell
# On EC2, use Docker MCP for container orchestration
gemini "Set up a production-like container environment on EC2"
```

### E2B Sandbox Integration

**Combine E2B and Docker:**
```powershell
# Use E2B sandbox to develop, Docker MCP to containerize
gemini "In E2B sandbox, create a Python app, then use Docker MCP to build and run it"
```

## Troubleshooting

### Issue: MCP Server Not Connected

**Symptoms:**
```
✗ MCP_DOCKER: docker mcp gateway run (stdio) - Disconnected
```

**Solutions:**
```powershell
# 1. Check Docker Desktop is running
docker ps

# 2. Start MCP Gateway
docker mcp gateway run

# 3. Restart Gemini CLI connection
# Exit and restart Gemini CLI
```

### Issue: Tools Not Available

**Symptoms:**
- Gemini CLI doesn't recognize Docker commands
- "Tool not found" errors

**Solutions:**
```powershell
# 1. Verify MCP server is connected
gemini mcp list

# 2. Test with simple command
gemini "List Docker containers"

# 3. Check Docker MCP Gateway logs
docker mcp gateway logs
```

### Issue: Permission Errors

**Symptoms:**
- "Permission denied" when managing containers

**Solutions:**
```powershell
# 1. Check Docker permissions
docker ps

# 2. Ensure user is in docker group (Linux)
sudo usermod -aG docker $USER

# 3. Restart Docker service if needed
```

### Issue: Resource Limits

**Symptoms:**
- Containers fail to start
- "Out of memory" errors

**Solutions:**
```powershell
# 1. Check Docker resource usage
gemini "Show Docker system information and disk usage"

# 2. Clean up resources
gemini "Prune unused Docker resources"

# 3. Adjust container resource limits
gemini "Create container with lower resource limits"
```

## Quick Reference

### Common Commands

```powershell
# Container Management
gemini "List containers"
gemini "Create container [name] with image [image]"
gemini "Start container [name]"
gemini "Stop container [name]"
gemini "Remove container [name]"
gemini "Get logs from container [name]"

# Image Management
gemini "List images"
gemini "Build image from Dockerfile"
gemini "Pull image [name]"
gemini "Push image [name]"
gemini "Remove image [name]"

# Volume Management
gemini "List volumes"
gemini "Create volume [name]"
gemini "Remove volume [name]"

# Network Management
gemini "List networks"
gemini "Create network [name]"
gemini "Connect container [name] to network [network]"

# Compose
gemini "Start docker-compose services"
gemini "Stop docker-compose services"
gemini "View docker-compose logs"

# System
gemini "Show Docker system info"
gemini "Show Docker disk usage"
gemini "Prune unused resources"
```

## Next Steps

1. **Explore MCP Catalog**: Browse available MCP servers in Docker Desktop
2. **Try Dynamic MCP**: Enable dynamic server discovery
3. **Build Custom Workflows**: Combine Docker MCP with other tools
4. **Automate Tasks**: Create scripts using Docker MCP tools
5. **Monitor Resources**: Set up monitoring for container resources

## Resources

- [Docker MCP Toolkit Documentation](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/)
- [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)
- [MCP Gateway Guide](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)
- [Dynamic MCP](https://docs.docker.com/ai/mcp-catalog-and-toolkit/dynamic-mcp/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

