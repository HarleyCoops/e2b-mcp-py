#!/bin/bash
# Gemini CLI Setup Script for macOS/Linux
# This script helps set up Gemini CLI for local, Docker, and EC2 usage

echo "=== Gemini CLI Setup ==="

# Check if Gemini CLI is installed
echo ""
echo "1. Checking Gemini CLI installation..."
if command -v gemini &> /dev/null; then
    VERSION=$(gemini --version 2>&1)
    echo "   OK Gemini CLI version: $VERSION"
else
    echo "   ERROR Gemini CLI not found. Install with: npm install -g @google/gemini-cli"
    exit 1
fi

# Check environment variables
echo ""
echo "2. Checking environment variables..."
REQUIRED_VARS=("GEMINI_API_KEY")
OPTIONAL_VARS=("E2B_API_KEY" "GITHUB_TOKEN" "NOTION_TOKEN" "ANTHROPIC_API_KEY")

MISSING=()
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING+=("$var")
    else
        VALUE="${!var}"
        PREVIEW="${VALUE:0:20}"
        echo "   OK $var = ${PREVIEW}..."
    fi
done

for var in "${OPTIONAL_VARS[@]}"; do
    if [ -n "${!var}" ]; then
        VALUE="${!var}"
        PREVIEW="${VALUE:0:20}"
        echo "   OK $var = ${PREVIEW}..."
    else
        echo "   INFO $var not set (optional)"
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo ""
    echo "   WARNING Missing required variables: ${MISSING[*]}"
    echo "   Set them with: export GEMINI_API_KEY='your-key'"
fi

# Check Docker
echo ""
echo "3. Checking Docker installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1)
    echo "   OK Docker: $DOCKER_VERSION"
    
    # Check if Docker is running
    if docker ps &> /dev/null; then
        echo "   OK Docker daemon is running"
    else
        echo "   WARNING Docker daemon may not be running"
    fi
else
    echo "   INFO Docker not found (optional for Docker usage)"
fi

# Check MCP servers
echo ""
echo "4. Checking MCP server configuration..."
if gemini mcp list &> /dev/null; then
    echo "   MCP Servers:"
    gemini mcp list
else
    echo "   INFO Could not list MCP servers"
fi

# Test Gemini CLI
echo ""
echo "5. Testing Gemini CLI connection..."
if [ -n "$GEMINI_API_KEY" ]; then
    if gemini "Say 'OK' if you can hear me" &> /dev/null; then
        echo "   OK Gemini CLI is working!"
    else
        echo "   WARNING Gemini CLI test failed"
    fi
else
    echo "   SKIP Cannot test without GEMINI_API_KEY"
fi

# Summary
echo ""
echo "=== Setup Summary ==="
echo "Local Usage:"
echo "  gemini                          # Interactive mode"
echo "  gemini 'your query'              # One-shot query"
echo "  gemini -s 'query'                # Sandbox mode"

if command -v docker &> /dev/null; then
    echo ""
    echo "Docker Usage:"
    echo "  docker build -f Dockerfile.gemini -t gemini-cli ."
    echo "  docker run -it --rm -e GEMINI_API_KEY=\$GEMINI_API_KEY gemini-cli"
    echo "  docker-compose -f docker-compose.gemini.yml run --rm gemini-cli"
fi

echo ""
echo "EC2 Usage:"
echo "  ssh -i key.pem ec2-user@your-ec2-ip"
echo "  gemini 'your query'"

echo ""
echo "For detailed instructions, see GEMINI.md"
echo ""
echo "Setup complete!"

