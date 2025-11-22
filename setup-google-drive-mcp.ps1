# Google Drive MCP Server Setup Script for Windows PowerShell
# This script helps set up Google Drive MCP server for Gemini CLI

Write-Host "=== Google Drive MCP Server Setup ===" -ForegroundColor Cyan

# Check prerequisites
Write-Host "`n1. Checking prerequisites..." -ForegroundColor Yellow

# Check npm
try {
    $npmVersion = npm --version 2>&1
    Write-Host "   OK npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "   ERROR npm not found. Please install Node.js first." -ForegroundColor Red
    exit 1
}

# Check Gemini CLI
try {
    $geminiVersion = gemini --version 2>&1
    Write-Host "   OK Gemini CLI version: $geminiVersion" -ForegroundColor Green
} catch {
    Write-Host "   ERROR Gemini CLI not found. Please install Gemini CLI first." -ForegroundColor Red
    exit 1
}

# Step 1: Install MCP Server
Write-Host "`n2. Installing Google Drive MCP server..." -ForegroundColor Yellow
Write-Host "   This will install @piotr-agier/google-drive-mcp globally" -ForegroundColor Gray

$installChoice = Read-Host "   Install now? (Y/n)"
if ($installChoice -ne "n" -and $installChoice -ne "N") {
    npm install -g @piotr-agier/google-drive-mcp
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK Google Drive MCP server installed" -ForegroundColor Green
    } else {
        Write-Host "   ERROR Installation failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   SKIP Installation skipped" -ForegroundColor Gray
}

# Step 2: OAuth Credentials Setup
Write-Host "`n3. Google Cloud OAuth Credentials Setup" -ForegroundColor Yellow
Write-Host "   You need to:" -ForegroundColor Cyan
Write-Host "   1. Go to https://console.cloud.google.com/" -ForegroundColor White
Write-Host "   2. Create/select a project" -ForegroundColor White
Write-Host "   3. Enable Google Drive API" -ForegroundColor White
Write-Host "   4. Configure OAuth consent screen" -ForegroundColor White
Write-Host "   5. Create OAuth Client ID (Desktop app)" -ForegroundColor White
Write-Host "   6. Download credentials JSON file" -ForegroundColor White

$credentialsPath = Read-Host "`n   Enter path to your OAuth credentials JSON file (or press Enter to skip)"
if ($credentialsPath -and (Test-Path $credentialsPath)) {
    # Set environment variable
    $env:GOOGLE_DRIVE_OAUTH_CREDENTIALS = $credentialsPath
    Write-Host "   OK Credentials path set: $credentialsPath" -ForegroundColor Green
    
    # Add to .env file
    if (Test-Path .env) {
        $envContent = Get-Content .env -Raw
        if ($envContent -notmatch "GOOGLE_DRIVE_OAUTH_CREDENTIALS") {
            Add-Content .env "`nGOOGLE_DRIVE_OAUTH_CREDENTIALS=$credentialsPath"
            Write-Host "   OK Added to .env file" -ForegroundColor Green
        } else {
            Write-Host "   INFO Already in .env file" -ForegroundColor Gray
        }
    } else {
        Write-Host "   INFO .env file not found, creating it..." -ForegroundColor Gray
        "GOOGLE_DRIVE_OAUTH_CREDENTIALS=$credentialsPath" | Out-File -FilePath .env -Encoding utf8
        Write-Host "   OK Created .env file" -ForegroundColor Green
    }
} else {
    Write-Host "   WARNING Credentials path not provided or file not found" -ForegroundColor Yellow
    Write-Host "   You'll need to set GOOGLE_DRIVE_OAUTH_CREDENTIALS environment variable manually" -ForegroundColor Yellow
}

# Step 3: Authentication
Write-Host "`n4. Authentication" -ForegroundColor Yellow
if ($env:GOOGLE_DRIVE_OAUTH_CREDENTIALS) {
    Write-Host "   Ready to authenticate!" -ForegroundColor Green
    Write-Host "   Run this command to authenticate:" -ForegroundColor Cyan
    Write-Host "   npx @piotr-agier/google-drive-mcp auth" -ForegroundColor White
    
    $authChoice = Read-Host "`n   Run authentication now? (Y/n)"
    if ($authChoice -ne "n" -and $authChoice -ne "N") {
        npx @piotr-agier/google-drive-mcp auth
    }
} else {
    Write-Host "   SKIP Cannot authenticate without credentials" -ForegroundColor Gray
    Write-Host "   Set GOOGLE_DRIVE_OAUTH_CREDENTIALS first, then run:" -ForegroundColor Yellow
    Write-Host "   npx @piotr-agier/google-drive-mcp auth" -ForegroundColor White
}

# Step 4: Add to Gemini CLI
Write-Host "`n5. Adding to Gemini CLI..." -ForegroundColor Yellow
if ($env:GOOGLE_DRIVE_OAUTH_CREDENTIALS) {
    Write-Host "   Adding Google Drive MCP server to Gemini CLI..." -ForegroundColor Gray
    
    # Try to add using gemini mcp add command
    gemini mcp add google-drive `
        --command "npx" `
        --args "-y", "@piotr-agier/google-drive-mcp" `
        --env "GOOGLE_DRIVE_OAUTH_CREDENTIALS=$env:GOOGLE_DRIVE_OAUTH_CREDENTIALS"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK Google Drive MCP server added to Gemini CLI" -ForegroundColor Green
    } else {
        Write-Host "   WARNING Could not add via command. You may need to edit config manually." -ForegroundColor Yellow
        Write-Host "   Config location: $env:APPDATA\gemini-cli\config.json" -ForegroundColor Gray
    }
} else {
    Write-Host "   SKIP Cannot add without credentials" -ForegroundColor Gray
    Write-Host "   After setting credentials, run:" -ForegroundColor Yellow
    Write-Host "   gemini mcp add google-drive --command npx --args -y,@piotr-agier/google-drive-mcp --env GOOGLE_DRIVE_OAUTH_CREDENTIALS=`$env:GOOGLE_DRIVE_OAUTH_CREDENTIALS" -ForegroundColor White
}

# Step 5: Verify
Write-Host "`n6. Verification" -ForegroundColor Yellow
Write-Host "   Checking MCP server configuration..." -ForegroundColor Gray
gemini mcp list

Write-Host "`n=== Setup Summary ===" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. If not done, set up Google Cloud OAuth credentials" -ForegroundColor White
Write-Host "2. Authenticate: npx @piotr-agier/google-drive-mcp auth" -ForegroundColor White
Write-Host "3. Test: gemini 'List files in my Google Drive'" -ForegroundColor White
Write-Host "`nFor detailed instructions, see GOOGLE-DRIVE-MCP-SETUP.md" -ForegroundColor Cyan
Write-Host "`nSetup complete!" -ForegroundColor Green

