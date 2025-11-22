# Gemini CLI Setup Script for Windows PowerShell
# This script helps set up Gemini CLI for local, Docker, and EC2 usage

Write-Host "=== Gemini CLI Setup ===" -ForegroundColor Cyan

# Check if Gemini CLI is installed
Write-Host "`n1. Checking Gemini CLI installation..." -ForegroundColor Yellow
try {
    $version = gemini --version 2>&1
    Write-Host "   OK Gemini CLI version: $version" -ForegroundColor Green
} catch {
    Write-Host "   ERROR Gemini CLI not found. Install with: npm install -g @google/gemini-cli" -ForegroundColor Red
    exit 1
}

# Check environment variables
Write-Host "`n2. Checking environment variables..." -ForegroundColor Yellow
$requiredVars = @("GEMINI_API_KEY")
$optionalVars = @("E2B_API_KEY", "GITHUB_TOKEN", "NOTION_TOKEN", "ANTHROPIC_API_KEY")

$missing = @()
foreach ($var in $requiredVars) {
    if (-not (Get-Item "Env:$var" -ErrorAction SilentlyContinue)) {
        $missing += $var
    } else {
        $value = (Get-Item "Env:$var").Value
        Write-Host "   OK $var = $($value.Substring(0, [Math]::Min(20, $value.Length)))..." -ForegroundColor Green
    }
}

foreach ($var in $optionalVars) {
    if (Get-Item "Env:$var" -ErrorAction SilentlyContinue) {
        $value = (Get-Item "Env:$var").Value
        Write-Host "   OK $var = $($value.Substring(0, [Math]::Min(20, $value.Length)))..." -ForegroundColor Green
    } else {
        Write-Host "   INFO $var not set (optional)" -ForegroundColor Gray
    }
}

if ($missing.Count -gt 0) {
    Write-Host "`n   WARNING Missing required variables: $($missing -join ', ')" -ForegroundColor Yellow
    Write-Host "   Set them with: `$env:GEMINI_API_KEY = 'your-key'" -ForegroundColor Yellow
}

# Check Docker
Write-Host "`n3. Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "   OK Docker: $dockerVersion" -ForegroundColor Green
    
    # Check if Docker is running
    docker ps | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK Docker daemon is running" -ForegroundColor Green
    } else {
        Write-Host "   WARNING Docker daemon may not be running" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   INFO Docker not found (optional for Docker usage)" -ForegroundColor Gray
}

# Check MCP servers
Write-Host "`n4. Checking MCP server configuration..." -ForegroundColor Yellow
try {
    $mcpList = gemini mcp list 2>&1
    Write-Host "   MCP Servers:" -ForegroundColor Cyan
    Write-Host $mcpList
} catch {
    Write-Host "   INFO Could not list MCP servers" -ForegroundColor Gray
}

# Test Gemini CLI
Write-Host "`n5. Testing Gemini CLI connection..." -ForegroundColor Yellow
if ($env:GEMINI_API_KEY) {
    try {
        $testResult = gemini "Say 'OK' if you can hear me" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   OK Gemini CLI is working!" -ForegroundColor Green
        } else {
            Write-Host "   WARNING Gemini CLI test failed" -ForegroundColor Yellow
            Write-Host $testResult
        }
    } catch {
        Write-Host "   WARNING Could not test Gemini CLI" -ForegroundColor Yellow
    }
} else {
    Write-Host "   SKIP Cannot test without GEMINI_API_KEY" -ForegroundColor Gray
}

# Summary
Write-Host "`n=== Setup Summary ===" -ForegroundColor Cyan
Write-Host "Local Usage:" -ForegroundColor Yellow
Write-Host "  gemini                          # Interactive mode"
Write-Host "  gemini 'your query'              # One-shot query"
Write-Host "  gemini -s 'query'                # Sandbox mode"

if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "`nDocker Usage:" -ForegroundColor Yellow
    Write-Host "  docker build -f Dockerfile.gemini -t gemini-cli ."
    Write-Host "  docker run -it --rm -e GEMINI_API_KEY=`$env:GEMINI_API_KEY gemini-cli"
    Write-Host "  docker-compose -f docker-compose.gemini.yml run --rm gemini-cli"
}

Write-Host "`nEC2 Usage:" -ForegroundColor Yellow
Write-Host "  ssh -i key.pem ec2-user@your-ec2-ip"
Write-Host "  gemini 'your query'"

Write-Host "`nFor detailed instructions, see GEMINI.md" -ForegroundColor Cyan
Write-Host "`nSetup complete!" -ForegroundColor Green

