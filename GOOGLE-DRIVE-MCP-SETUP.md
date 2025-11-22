# Google Drive MCP Server Setup Guide

Complete guide for installing and configuring a Google Drive MCP server with Gemini CLI.

## Overview

You can install a Google Drive MCP server to enable Gemini CLI to interact with your Google Drive files, folders, and documents. There are multiple options available.

## Option 1: @piotr-agier/google-drive-mcp (Recommended)

This is a well-maintained npm package that provides Google Drive, Docs, Sheets, and Slides integration.

### Step 1: Install the MCP Server Package

```powershell
# Install globally via npm
npm install -g @piotr-agier/google-drive-mcp

# Or use npx (no installation needed)
# npx @piotr-agier/google-drive-mcp
```

### Step 2: Set Up Google Cloud OAuth Credentials

1. **Go to Google Cloud Console:**
   - Visit https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project:**
   - Click "Select a project" → "New Project"
   - Give it a name (e.g., "Gemini CLI Google Drive")
   - Click "Create"

3. **Enable Google Drive API:**
   - Go to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

4. **Configure OAuth Consent Screen:**
   - Go to "APIs & Services" → "OAuth consent screen"
   - Choose "Internal" (for personal use) or "External" (for wider use)
   - Fill in required fields:
     - App name: "Gemini CLI Google Drive"
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - Add scopes (if needed):
     - `https://www.googleapis.com/auth/drive.readonly` (read-only)
     - `https://www.googleapis.com/auth/drive` (full access)
   - Click "Save and Continue"
   - Add test users (if using External)
   - Click "Save and Continue"

5. **Create OAuth Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Gemini CLI Google Drive"
   - Click "Create"
   - Download the JSON file
   - Save it as `gcp-oauth.keys.json` in a secure location

### Step 3: Set Environment Variable

**PowerShell:**
```powershell
# Set the path to your OAuth credentials file
$env:GOOGLE_DRIVE_OAUTH_CREDENTIALS = "C:\path\to\gcp-oauth.keys.json"

# Or add to .env file
Add-Content .env "GOOGLE_DRIVE_OAUTH_CREDENTIALS=C:\path\to\gcp-oauth.keys.json"
```

**Bash:**
```bash
export GOOGLE_DRIVE_OAUTH_CREDENTIALS="/path/to/gcp-oauth.keys.json"
```

### Step 4: Authenticate

```powershell
# Run authentication command
npx @piotr-agier/google-drive-mcp auth

# Follow the prompts:
# 1. It will open a browser window
# 2. Sign in with your Google account
# 3. Grant permissions
# 4. Copy the authorization code
# 5. Paste it back into the terminal
```

### Step 5: Add to Gemini CLI

**Using Gemini CLI MCP commands:**
```powershell
# Add Google Drive MCP server
gemini mcp add google-drive `
  --command "npx" `
  --args "-y", "@piotr-agier/google-drive-mcp" `
  --env "GOOGLE_DRIVE_OAUTH_CREDENTIALS=$env:GOOGLE_DRIVE_OAUTH_CREDENTIALS"
```

**Or manually edit Gemini CLI config:**
The config file is typically at:
- **Windows:** `%APPDATA%\gemini-cli\config.json`
- **macOS/Linux:** `~/.config/gemini-cli/config.json`

Add this configuration:
```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@piotr-agier/google-drive-mcp"],
      "env": {
        "GOOGLE_DRIVE_OAUTH_CREDENTIALS": "C:\\path\\to\\gcp-oauth.keys.json"
      }
    }
  }
}
```

### Step 6: Verify Installation

```powershell
# List MCP servers
gemini mcp list

# Should show:
# ✓ google-drive: npx -y @piotr-agier/google-drive-mcp - Connected

# Test with a simple command
gemini "List files in my Google Drive"
```

## Option 2: @isaacphi/mcp-gdrive (Alternative)

Another option using a different implementation.

### Installation

```powershell
# Install via npm
npm install -g @isaacphi/mcp-gdrive

# Or use npx
# npx -y @isaacphi/mcp-gdrive
```

### Configuration

You'll need to set up OAuth credentials similar to Option 1, then configure:

```powershell
gemini mcp add gdrive `
  --command "npx" `
  --args "-y", "@isaacphi/mcp-gdrive" `
  --env "CLIENT_ID=your-client-id", "CLIENT_SECRET=your-client-secret", "GDRIVE_CREDS_DIR=C:\path\to\config"
```

## Option 3: Python-based MCP Server

If you prefer Python:

```bash
# Clone repository
git clone https://github.com/isaacphi/mcp-gdrive.git
cd mcp-gdrive

# Install dependencies
pip install -e .

# Set up authentication
python -m gdrive_mcp_server.auth_setup \
  --credentials /path/to/credentials.json \
  --token /path/to/tokens.json

# Run server
gdrive-mcp
```

## Available Google Drive MCP Tools

Once configured, Gemini CLI will have access to tools like:

- **List Files**: List files and folders in Google Drive
- **Read Files**: Read content from Google Drive files
- **Search**: Search for files by name or content
- **Upload**: Upload files to Google Drive
- **Create Folders**: Create new folders
- **Share Files**: Share files with others
- **Download**: Download files from Google Drive
- **Google Docs**: Read and edit Google Docs
- **Google Sheets**: Read and edit Google Sheets
- **Google Slides**: Read and edit Google Slides

## Usage Examples

### Basic Operations

```powershell
# List files in root directory
gemini "List all files in my Google Drive root folder"

# Search for files
gemini "Search for files containing 'project' in my Google Drive"

# Read a file
gemini "Read the content of 'My Document.docx' from Google Drive"

# Upload a file
gemini "Upload the file 'report.pdf' to Google Drive"
```

### Advanced Operations

```powershell
# Work with Google Docs
gemini "Create a new Google Doc called 'Meeting Notes' and add some content"

# Work with Google Sheets
gemini "Read data from my Google Sheet 'Budget 2024'"

# Organize files
gemini "Create a folder called 'Projects' and move all files with 'project' in the name to it"

# Share files
gemini "Share the file 'Report.pdf' with read access to user@example.com"
```

### Integration with Other Tools

```powershell
# Combine with Docker MCP
gemini "Create a Docker container, generate a report, and upload it to Google Drive"

# Combine with GitHub MCP
gemini "Clone a GitHub repo, analyze it, create a summary document, and upload to Google Drive"

# Combine with E2B sandbox
gemini "Run a Python script in E2B sandbox, generate results, and save to Google Drive"
```

## Troubleshooting

### Issue: Authentication Fails

**Symptoms:**
- "Authentication failed" errors
- Browser doesn't open

**Solutions:**
```powershell
# 1. Verify credentials file path
echo $env:GOOGLE_DRIVE_OAUTH_CREDENTIALS

# 2. Check file exists and is readable
Test-Path $env:GOOGLE_DRIVE_OAUTH_CREDENTIALS

# 3. Re-run authentication
npx @piotr-agier/google-drive-mcp auth
```

### Issue: MCP Server Not Connecting

**Symptoms:**
- Server shows as disconnected
- Tools not available

**Solutions:**
```powershell
# 1. Check MCP server status
gemini mcp list

# 2. Verify npm/npx is available
npx --version

# 3. Test server manually
npx -y @piotr-agier/google-drive-mcp

# 4. Check environment variables
echo $env:GOOGLE_DRIVE_OAUTH_CREDENTIALS
```

### Issue: Permission Denied

**Symptoms:**
- "Permission denied" errors
- Can't access files

**Solutions:**
1. Check OAuth scopes in Google Cloud Console
2. Re-authenticate with broader permissions
3. Verify file sharing settings in Google Drive

### Issue: API Not Enabled

**Symptoms:**
- "API not enabled" errors

**Solutions:**
1. Go to Google Cloud Console
2. Enable Google Drive API
3. Wait a few minutes for propagation
4. Re-authenticate

## Security Best Practices

1. **Store Credentials Securely:**
   - Don't commit `gcp-oauth.keys.json` to git
   - Use environment variables
   - Add to `.gitignore`

2. **Use Least Privilege:**
   - Only request necessary OAuth scopes
   - Use read-only access when possible

3. **Rotate Credentials:**
   - Regularly rotate OAuth credentials
   - Revoke unused credentials

4. **Monitor Access:**
   - Review OAuth consent screen regularly
   - Check Google Account security settings

## Quick Reference

### Installation Commands

```powershell
# Install package
npm install -g @piotr-agier/google-drive-mcp

# Set credentials path
$env:GOOGLE_DRIVE_OAUTH_CREDENTIALS = "C:\path\to\gcp-oauth.keys.json"

# Authenticate
npx @piotr-agier/google-drive-mcp auth

# Add to Gemini CLI
gemini mcp add google-drive `
  --command "npx" `
  --args "-y", "@piotr-agier/google-drive-mcp" `
  --env "GOOGLE_DRIVE_OAUTH_CREDENTIALS=$env:GOOGLE_DRIVE_OAUTH_CREDENTIALS"

# Verify
gemini mcp list
gemini "List files in my Google Drive"
```

### Common Commands

```powershell
# List files
gemini "List files in Google Drive"

# Search
gemini "Search for 'budget' files in Google Drive"

# Read file
gemini "Read 'My Document.docx' from Google Drive"

# Upload
gemini "Upload 'report.pdf' to Google Drive"

# Create folder
gemini "Create folder 'Projects' in Google Drive"
```

## Resources

- **@piotr-agier/google-drive-mcp**: https://github.com/piotr-agier/google-drive-mcp
- **@isaacphi/mcp-gdrive**: https://github.com/isaacphi/mcp-gdrive
- **Google Cloud Console**: https://console.cloud.google.com/
- **Google Drive API Docs**: https://developers.google.com/drive/api
- **MCP Protocol**: https://modelcontextprotocol.io/

## Next Steps

1. Choose an MCP server option (recommend Option 1)
2. Set up Google Cloud OAuth credentials
3. Install and authenticate the MCP server
4. Add to Gemini CLI configuration
5. Test with simple commands
6. Explore advanced features
7. Integrate with other MCP servers (Docker, GitHub, Notion)

