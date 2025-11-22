# Gemini CLI Quick Start Guide

Quick reference for getting started with Gemini CLI in your e2b-mcp-py project.

## Prerequisites

- Gemini CLI installed (v0.17.1+) ✓
- Docker installed and running ✓
- GEMINI_API_KEY configured

## Quick Setup

### 1. Set Your API Key

**PowerShell:**
```powershell
# Option 1: Set in current session
$env:GEMINI_API_KEY = "your-key-here"

# Option 2: Add to .env file (recommended)
Add-Content .env "GEMINI_API_KEY=your-key-here"
```

**Bash:**
```bash
# Option 1: Set in current session
export GEMINI_API_KEY="your-key-here"

# Option 2: Add to .env file (recommended)
echo "GEMINI_API_KEY=your-key-here" >> .env
```

### 2. Run Setup Script

**PowerShell:**
```powershell
.\setup-gemini.ps1
```

**Bash:**
```bash
chmod +x setup-gemini.sh
./setup-gemini.sh
```

## Usage Modes

### Local Mode (Fast Iteration)

```powershell
# Interactive mode
gemini

# One-shot query
gemini "What files are in this directory?"

# With helper script (loads .env automatically)
.\run-gemini.ps1 "Analyze the project structure"
```

### Sandbox Mode (Safe Execution)

```powershell
# Run in E2B sandbox
gemini -s "Create a Python script to analyze GitHub repos"

# Interactive sandbox mode
gemini -s -i "Build a feature"
```

### Docker Mode (Consistent Environment)

```powershell
# Build Docker image
docker build -f Dockerfile.gemini -t gemini-cli .

# Run interactively
docker run -it --rm `
  -e GEMINI_API_KEY="$env:GEMINI_API_KEY" `
  -v ${PWD}:/workspace `
  -w /workspace `
  gemini-cli

# Run with docker-compose (loads .env automatically)
docker-compose -f docker-compose.gemini.yml run --rm gemini-cli "Your query"
```

### EC2 Mode (Production)

```bash
# SSH into EC2
ssh -i key.pem ec2-user@your-ec2-ip

# Run Gemini CLI
gemini "Your query"
```

## Common Commands

### Project Analysis

```powershell
# Analyze codebase
gemini "Analyze the project structure and suggest improvements"

# Review specific files
gemini "Review deep_agent.py and suggest optimizations"

# Understand architecture
gemini "Explain how the E2B sandbox integration works"
```

### Code Generation

```powershell
# Generate code
gemini -s "Create a Python script to sync GitHub issues to Notion"

# Refactor code
gemini "Refactor the examples.py file to use async/await"

# Write tests
gemini "Write unit tests for deep_agent.py"
```

### Integration Tasks

```powershell
# Work with GitHub
gemini "List my GitHub repositories and analyze them"

# Work with Notion
gemini "Create a Notion database for tracking project tasks"

# Combine services
gemini "Sync GitHub issues to a Notion database"
```

## MCP Server Usage

### List Available Servers

```powershell
gemini mcp list
```

### Use Docker MCP (Already Configured)

```powershell
# Gemini CLI can manage Docker containers
gemini "List all running Docker containers"

gemini "Build a Docker image for this project"

gemini "Create a container with Python 3.13"
```

### Add More MCP Servers

```powershell
# GitHub MCP
gemini mcp add github `
  --command "npx -y @modelcontextprotocol/server-github" `
  --env "GITHUB_TOKEN=$env:GITHUB_TOKEN"

# Notion MCP
gemini mcp add notion `
  --command "npx -y @modelcontextprotocol/server-notion" `
  --env "NOTION_TOKEN=$env:NOTION_TOKEN"
```

## Workflow Examples

### Development Workflow

```powershell
# 1. Plan locally
gemini "Design a feature to add MCP server builder"

# 2. Test in Docker
docker-compose -f docker-compose.gemini.yml run --rm gemini-cli `
  "Implement the MCP server builder feature"

# 3. Execute in sandbox
gemini -s "Test the MCP server builder with a sample API"
```

### Integration Workflow

```powershell
# Combine Gemini CLI with your existing tools
gemini "Use the deep_agent.py to analyze GitHub repos and create a summary"

# Run your Python scripts through Gemini
gemini "Execute: uv run examples.py github"
```

### Production Workflow

```powershell
# 1. Develop locally
gemini "Create deployment script"

# 2. Test in Docker
docker-compose -f docker-compose.gemini.yml run --rm gemini-cli `
  "Test the deployment script"

# 3. Deploy to EC2
# SSH to EC2 and run the same commands
```

## Tips for Maximizing Usage

### 1. Use the Right Mode for the Task

- **Local**: Quick questions, code review, planning
- **Sandbox**: Code execution, testing, safe experimentation
- **Docker**: Consistent testing, CI/CD, reproducible environments
- **EC2**: Long-running tasks, production workloads, persistent state

### 2. Combine with Your Existing Tools

```powershell
# Gemini CLI can orchestrate your Python scripts
gemini "Run the GitHub example and analyze the results"

# Use Gemini CLI to enhance your E2B workflows
gemini -s "Use E2B sandbox to run examples.py and create a report"
```

### 3. Leverage MCP Servers

```powershell
# Docker MCP: Container management
gemini "Create a Docker container for testing"

# GitHub MCP: Repository operations
gemini "Create a new branch and open a PR"

# Notion MCP: Documentation
gemini "Create a Notion page documenting this project"
```

### 4. Use Helper Scripts

```powershell
# Load .env automatically
.\run-gemini.ps1 "Your query"

# Run setup check
.\setup-gemini.ps1
```

## Troubleshooting

### API Key Not Set

```powershell
# Check if set
echo $env:GEMINI_API_KEY

# Set it
$env:GEMINI_API_KEY = "your-key"
# Or use .env file with run-gemini.ps1
```

### Docker Issues

```powershell
# Check Docker is running
docker ps

# Rebuild image
docker build -f Dockerfile.gemini -t gemini-cli .
```

### Sandbox Issues

```powershell
# Verify E2B API key
echo $env:E2B_API_KEY

# Test sandbox
gemini -s "List sandbox information"
```

## Next Steps

1. **Read Full Guide**: See `GEMINI.md` for comprehensive documentation
2. **Configure MCP Servers**: Add GitHub, Notion, and other integrations
3. **Set Up Docker**: Use docker-compose for easy development
4. **EC2 Setup**: Install Gemini CLI on your EC2 instance
5. **Create Workflows**: Build scripts to automate common tasks

## Resources

- **Full Documentation**: `GEMINI.md`
- **Project README**: `README.md`
- **Setup Guide**: `SETUP.md`
- **Gemini CLI Docs**: https://www.geminicli.click/
- **MCP Protocol**: https://modelcontextprotocol.io/

