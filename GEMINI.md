# Gemini CLI Setup & Integration Guide

Complete guide for setting up and maximizing Gemini CLI usage across local, Docker, and EC2 sandbox environments.

## Table of Contents

1. [Local Setup](#local-setup)
2. [Docker Integration](#docker-integration)
3. [EC2 Sandbox Integration](#ec2-sandbox-integration)
4. [Maximizing Usage Across Environments](#maximizing-usage-across-environments)
5. [MCP Server Configuration](#mcp-server-configuration)
6. [Best Practices](#best-practices)

## Local Setup

### Prerequisites

- Gemini CLI installed (v0.17.1+)
- GEMINI_API_KEY configured
- Node.js 18+ (if installing from npm)

### Authentication

Gemini CLI uses the `GEMINI_API_KEY` environment variable for authentication. Configure it in your `.env` file:

```powershell
# Windows PowerShell
$env:GEMINI_API_KEY = "your-gemini-api-key-here"
# Or add to .env file
```

```bash
# macOS/Linux
export GEMINI_API_KEY="your-gemini-api-key-here"
# Or add to .env file
```

### Verify Installation

```powershell
# Check version
gemini --version

# Test authentication
gemini "Hello, can you confirm you're working?"

# List configured MCP servers
gemini mcp list
```

### Basic Usage

**Interactive Mode:**
```powershell
gemini
```

**One-shot Query:**
```powershell
gemini "What files are in this directory?"
```

**Interactive Prompt:**
```powershell
gemini -i "Analyze the project structure"
```

**Sandbox Mode (E2B):**
```powershell
gemini -s "Run a Python script to analyze the codebase"
```

### Configuration File

Gemini CLI stores configuration in:
- **Windows:** `%APPDATA%\gemini-cli\config.json`
- **macOS/Linux:** `~/.config/gemini-cli/config.json`

You can customize:
- Default model
- MCP server configurations
- Extension settings
- Approval modes

## Docker Integration

### Option 1: Run Gemini CLI Inside Docker Container

Create a `Dockerfile.gemini`:

```dockerfile
FROM node:18-alpine

# Install Gemini CLI globally
RUN npm install -g @google/gemini-cli

# Set working directory
WORKDIR /workspace

# Copy project files
COPY . .

# Set environment variables (use --env-file or -e flags at runtime)
ENV GEMINI_API_KEY=""

# Default command
CMD ["gemini"]
```

**Build and Run:**

```powershell
# Build image
docker build -f Dockerfile.gemini -t gemini-cli:latest .

# Run interactively with environment variables
docker run -it --rm `
  -e GEMINI_API_KEY="$env:GEMINI_API_KEY" `
  -v ${PWD}:/workspace `
  -w /workspace `
  gemini-cli:latest

# Run with one-shot command
docker run -it --rm `
  -e GEMINI_API_KEY="$env:GEMINI_API_KEY" `
  -v ${PWD}:/workspace `
  -w /workspace `
  gemini-cli:latest "Analyze this codebase"
```

### Option 2: Docker Compose for Development

Create `docker-compose.gemini.yml`:

```yaml
version: '3.8'

services:
  gemini-cli:
    build:
      context: .
      dockerfile: Dockerfile.gemini
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - E2B_API_KEY=${E2B_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - NOTION_TOKEN=${NOTION_TOKEN}
    volumes:
      - .:/workspace
      - gemini-config:/root/.config/gemini-cli
    working_dir: /workspace
    stdin_open: true
    tty: true
    command: gemini

volumes:
  gemini-config:
```

**Usage:**

```powershell
# Start interactive session
docker-compose -f docker-compose.gemini.yml run --rm gemini-cli

# Run one-shot command
docker-compose -f docker-compose.gemini.yml run --rm gemini-cli "List all Python files"
```

### Option 3: Use Docker MCP Server (Already Configured)

You already have the Docker MCP server configured! This allows Gemini CLI to interact with Docker containers directly.

**Available Docker MCP Tools:**
- Container management
- Image building
- Volume management
- Network operations

**Example Usage:**

```powershell
# Gemini CLI can now manage Docker containers
gemini "List all running Docker containers"

gemini "Build a Docker image for this project"

gemini "Create a Docker container with Python 3.13"
```

## EC2 Sandbox Integration

### Option 1: Run Gemini CLI on EC2 Instance

**SSH into EC2:**

```powershell
# From your local machine
ssh -i path/to/key.pem ec2-user@your-ec2-ip
```

**Install Gemini CLI on EC2:**

```bash
# Install Node.js (Amazon Linux 2)
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Install Gemini CLI
sudo npm install -g @google/gemini-cli

# Set environment variables
export GEMINI_API_KEY="your-key-here"
echo "export GEMINI_API_KEY=\"your-key-here\"" >> ~/.bashrc

# Verify
gemini --version
```

**Run Gemini CLI on EC2:**

```bash
# Interactive mode
gemini

# One-shot with sandbox
gemini -s "Analyze the E2B project structure"
```

### Option 2: Use E2B Sandbox with Gemini CLI

Your project already uses E2B sandboxes! You can leverage this with Gemini CLI:

**Configure E2B Sandbox Mode:**

```powershell
# Set E2B API key
$env:E2B_API_KEY = "your-e2b-key"

# Run Gemini CLI with E2B sandbox
gemini -s "Create a Python script to analyze GitHub repositories"
```

**Integration with Your E2B Project:**

Since you have `deep_agent.py` that uses E2B sandboxes, you can:

1. **Use Gemini CLI to interact with E2B sandboxes:**
   ```powershell
   gemini -s "Use the E2B sandbox to run the examples.py script"
   ```

2. **Combine Gemini CLI with your existing E2B tools:**
   ```powershell
   # Gemini CLI can call your Python scripts that use E2B
   gemini "Run the GitHub example using uv run examples.py github"
   ```

### Option 3: Docker on EC2

**Install Docker on EC2:**

```bash
# Amazon Linux 2
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Log out and back in for group changes
exit
```

**Run Gemini CLI in Docker on EC2:**

```bash
# Build and run
docker build -f Dockerfile.gemini -t gemini-cli:latest .
docker run -it --rm \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  -v $(pwd):/workspace \
  -w /workspace \
  gemini-cli:latest
```

## Maximizing Usage Across Environments

### Strategy 1: Local Development + Docker Testing

**Workflow:**
1. Develop locally with Gemini CLI
2. Test in Docker containers for consistency
3. Deploy to EC2 for production workloads

**Example:**

```powershell
# Local: Quick iterations
gemini "Refactor this function"

# Docker: Test in isolated environment
docker run -it --rm `
  -e GEMINI_API_KEY="$env:GEMINI_API_KEY" `
  -v ${PWD}:/workspace `
  gemini-cli:latest "Test the refactored code"

# EC2: Production deployment
# SSH to EC2 and run same commands
```

### Strategy 2: E2B Sandbox for Code Execution

**Use Gemini CLI with E2B Sandbox Mode:**

```powershell
# Enable sandbox mode for safe code execution
gemini -s "Write and test a Python script"

# Combine with your existing E2B tools
gemini -s "Use the deep_agent.py to analyze GitHub repos"
```

**Benefits:**
- Isolated execution environment
- No local resource usage
- Consistent across all machines
- Automatic cleanup

### Strategy 3: MCP Server Integration

**Configure Multiple MCP Servers:**

```powershell
# List available MCP servers
gemini mcp list

# Your current setup includes:
# - MCP_DOCKER: Docker management
# - (Can add GitHub, Notion, etc.)
```

**Add GitHub MCP Server:**

```powershell
# Configure GitHub MCP (if you have the server)
gemini mcp add github --command "npx -y @modelcontextprotocol/server-github" --env GITHUB_TOKEN="$env:GITHUB_TOKEN"
```

**Add Notion MCP Server:**

```powershell
# Configure Notion MCP
gemini mcp add notion --command "npx -y @modelcontextprotocol/server-notion" --env NOTION_TOKEN="$env:NOTION_TOKEN"
```

### Strategy 4: Hybrid Approach

**Local + Docker + EC2 + E2B:**

```powershell
# 1. Local: Planning and design
gemini "Design a feature to sync GitHub issues to Notion"

# 2. Docker: Test implementation
docker-compose -f docker-compose.gemini.yml run --rm gemini-cli "Implement the sync feature"

# 3. E2B Sandbox: Execute safely
gemini -s "Run the sync script with test data"

# 4. EC2: Production deployment
# Deploy to EC2 and run with monitoring
```

## MCP Server Configuration

### Current Configuration

You have `MCP_DOCKER` configured. To see details:

```powershell
gemini mcp list
```

### Adding More MCP Servers

**GitHub MCP:**

```powershell
gemini mcp add github `
  --command "npx -y @modelcontextprotocol/server-github" `
  --env "GITHUB_TOKEN=$env:GITHUB_TOKEN"
```

**Notion MCP:**

```powershell
gemini mcp add notion `
  --command "npx -y @modelcontextprotocol/server-notion" `
  --env "NOTION_TOKEN=$env:NOTION_TOKEN"
```

**Custom MCP Server:**

```powershell
gemini mcp add custom-server `
  --command "python /path/to/mcp_server.py" `
  --env "API_KEY=$env:API_KEY"
```

### Managing MCP Servers

```powershell
# List all servers
gemini mcp list

# Remove a server
gemini mcp remove server-name

# Test a server
gemini mcp test server-name
```

## Best Practices

### 1. Environment Management

**Use .env files:**
```powershell
# Load environment variables
Get-Content .env | ForEach-Object {
    $name, $value = $_ -split '=', 2
    [Environment]::SetEnvironmentVariable($name, $value, "Process")
}
```

**Docker:**
```powershell
# Use --env-file
docker run -it --rm --env-file .env gemini-cli:latest
```

### 2. Resource Optimization

**Local:**
- Use for quick iterations
- Limited by local resources

**Docker:**
- Consistent environments
- Resource limits via Docker
- Easy cleanup

**E2B Sandbox:**
- Unlimited resources (cloud)
- Automatic cleanup
- Best for heavy workloads

**EC2:**
- Persistent environment
- Full control
- Best for long-running tasks

### 3. Security

**Never commit API keys:**
```powershell
# .env is in .gitignore
# Always use environment variables
$env:GEMINI_API_KEY = "key"
```

**Docker secrets:**
```powershell
# Use Docker secrets or environment variables
# Never hardcode in Dockerfile
```

**EC2:**
```bash
# Use AWS Secrets Manager or environment variables
# Restrict SSH access
# Use IAM roles when possible
```

### 4. Workflow Optimization

**Development Loop:**
1. Local: Fast feedback
2. Docker: Consistency check
3. E2B: Safe execution
4. EC2: Production ready

**Example Script:**

```powershell
# dev.ps1
param([string]$Task)

Write-Host "1. Local planning..."
gemini $Task

Write-Host "2. Docker testing..."
docker run -it --rm `
  -e GEMINI_API_KEY="$env:GEMINI_API_KEY" `
  -v ${PWD}:/workspace `
  gemini-cli:latest $Task

Write-Host "3. E2B sandbox execution..."
gemini -s $Task
```

### 5. Monitoring and Logging

**Local:**
```powershell
# Enable debug mode
gemini -d "Your task"

# Save output
gemini "Your task" | Tee-Object -FilePath output.log
```

**Docker:**
```powershell
# Capture logs
docker run --rm `
  -e GEMINI_API_KEY="$env:GEMINI_API_KEY" `
  gemini-cli:latest "Task" `
  | Tee-Object -FilePath docker-output.log
```

**EC2:**
```bash
# Use systemd or supervisor for logging
# Monitor with CloudWatch
```

## Troubleshooting

### Authentication Issues

```powershell
# Verify API key is set
echo $env:GEMINI_API_KEY

# Test authentication
gemini "Test"
```

### Docker Issues

```powershell
# Check Docker is running
docker ps

# Rebuild image
docker build -f Dockerfile.gemini -t gemini-cli:latest .
```

### E2B Sandbox Issues

```powershell
# Verify E2B API key
echo $env:E2B_API_KEY

# Test E2B connection
gemini -s "List sandbox information"
```

### EC2 Connection Issues

```powershell
# Test SSH connection
ssh -i key.pem ec2-user@ip

# Check Gemini CLI installation
ssh -i key.pem ec2-user@ip "gemini --version"
```

## Quick Reference

### Local Commands

```powershell
gemini                          # Interactive mode
gemini "query"                  # One-shot
gemini -i "query"               # Interactive prompt
gemini -s "query"               # Sandbox mode
gemini -d "query"               # Debug mode
gemini mcp list                 # List MCP servers
```

### Docker Commands

```powershell
docker build -f Dockerfile.gemini -t gemini-cli .
docker run -it --rm -e GEMINI_API_KEY="$env:GEMINI_API_KEY" gemini-cli:latest
docker-compose -f docker-compose.gemini.yml run --rm gemini-cli
```

### EC2 Commands

```bash
gemini --version                # Verify installation
export GEMINI_API_KEY="key"     # Set API key
gemini -s "query"                # Run with sandbox
```

## Next Steps

1. **Configure MCP Servers:** Add GitHub, Notion, and other integrations
2. **Set Up Docker:** Create docker-compose.yml for easy development
3. **EC2 Setup:** Install and configure Gemini CLI on your EC2 instance
4. **Create Workflows:** Build scripts to maximize usage across environments
5. **Integrate with E2B:** Combine Gemini CLI with your existing E2B sandbox tools

## Resources

- [Gemini CLI Documentation](https://www.geminicli.click/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [E2B Documentation](https://e2b.dev/docs)
- [Docker Documentation](https://docs.docker.com/)
