# Setup Guide - Deep Agent E2B

This guide provides detailed, step-by-step instructions for setting up the Deep Agent E2B project from scratch.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.13 or higher installed
- [ ] `uv` package manager installed (v0.4+)
- [ ] Git installed
- [ ] Access to create API keys for:
  - [ ] Anthropic (Claude)
  - [ ] E2B
  - [ ] GitHub (recommended)
  - [ ] Notion (optional)

## Step 1: Install Python and uv

### Python 3.13+

**Windows:**
```powershell
# Download from python.org or use winget
winget install Python.Python.3.13
```

**macOS:**
```bash
# Using Homebrew
brew install python@3.13

# Or download from python.org
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.13 python3.13-venv

# Fedora
sudo dnf install python3.13
```

Verify installation:
```bash
python --version  # Should show Python 3.13.x
```

### Install uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Or using pip:**
```bash
pip install uv
```

Verify installation:
```bash
uv --version  # Should show 0.4.x or higher
```

## Step 2: Clone the Repository

```bash
git clone https://github.com/e2b-dev/e2b-mcp-py
cd e2b-mcp-py
```

## Step 3: Install Dependencies

```bash
# This will create .venv and install all dependencies
uv sync
```

Expected output:
```
Creating virtual environment at .venv
Installing dependencies...
✓ Installed e2b
✓ Installed deepagents
✓ Installed langchain
...
```

Verify installation:
```bash
uv run python -c "import deep_agent, e2b; print('Setup complete!')"
```

## Step 4: Obtain API Keys

### 4.1 Anthropic API Key

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-api03-`)
6. **Important**: Save it immediately - you won't be able to see it again

### 4.2 E2B API Key

1. Visit https://e2b.dev/dashboard
2. Sign up or log in
3. Navigate to **API Keys** section
4. Copy your API key
5. If you don't have one, create a new API key

### 4.3 GitHub Personal Access Token

1. Visit https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Give it a descriptive name (e.g., "E2B Deep Agent")
4. Set expiration (recommended: 90 days or custom)
5. Select the following scopes:
   - [x] `repo` (Full control of private repositories)
   - [x] `read:user` (Read user profile data)
   - [x] `read:org` (Read org and team membership)
6. Click **Generate token**
7. Copy the token (starts with `ghp_`)
8. **Important**: Save it immediately - you won't be able to see it again

### 4.4 Notion Integration Token (Optional)

1. Visit https://www.notion.so/profile/integrations
2. Click **+ New integration**
3. Give it a name (e.g., "E2B Deep Agent")
4. Select your workspace
5. Click **Submit**
6. Copy the **Internal Integration Token** (starts with `secret_`)
7. **Share pages**: For the agent to access Notion pages, you need to:
   - Open the Notion page you want to share
   - Click the **...** menu (top right)
   - Click **Add connections**
   - Select your integration

## Step 5: Configure Environment Variables

Create a `.env` file in the project root:

**Windows (PowerShell):**
```powershell
@"
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
E2B_API_KEY=your_e2b_api_key_here
GITHUB_TOKEN=ghp_YOUR_TOKEN_HERE
NOTION_TOKEN=secret_YOUR_TOKEN_HERE
"@ | Out-File -FilePath .env -Encoding utf8
```

**macOS/Linux:**
```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
E2B_API_KEY=your_e2b_api_key_here
GITHUB_TOKEN=ghp_YOUR_TOKEN_HERE
NOTION_TOKEN=secret_YOUR_TOKEN_HERE
EOF
```

**Or manually create `.env` file:**
```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
E2B_API_KEY=your_e2b_api_key_here
GITHUB_TOKEN=ghp_YOUR_TOKEN_HERE
NOTION_TOKEN=secret_YOUR_TOKEN_HERE
```

**Important Notes:**
- Replace `YOUR_KEY_HERE` with your actual keys
- Do NOT commit `.env` to git (it's already in `.gitignore`)
- The `NOTION_TOKEN` line is optional - remove it if you're not using Notion

## Step 6: Verify Configuration

Run the verification script:

**Windows (PowerShell):**
```powershell
uv run python -c "
import os
from dotenv import load_dotenv
load_dotenv()
required = ['ANTHROPIC_API_KEY', 'E2B_API_KEY', 'GITHUB_TOKEN']
missing = [name for name in required if not os.getenv(name)]
if missing:
    print(f'Missing required keys: {missing}')
    exit(1)
print('✓ All required keys are present')
print(f'✓ Anthropic key: {os.getenv(\"ANTHROPIC_API_KEY\")[:20]}...')
print(f'✓ E2B key: {os.getenv(\"E2B_API_KEY\")[:20]}...')
print(f'✓ GitHub token: {os.getenv(\"GITHUB_TOKEN\")[:10]}...')
if os.getenv('NOTION_TOKEN'):
    print(f'✓ Notion token: {os.getenv(\"NOTION_TOKEN\")[:10]}...')
else:
    print('ℹ Notion token not set (optional)')
"
```

**macOS/Linux:**
```bash
uv run python -c "
import os
from dotenv import load_dotenv
load_dotenv()
required = ['ANTHROPIC_API_KEY', 'E2B_API_KEY', 'GITHUB_TOKEN']
missing = [name for name in required if not os.getenv(name)]
if missing:
    print(f'Missing required keys: {missing}')
    exit(1)
print('✓ All required keys are present')
print(f'✓ Anthropic key: {os.getenv(\"ANTHROPIC_API_KEY\")[:20]}...')
print(f'✓ E2B key: {os.getenv(\"E2B_API_KEY\")[:20]}...')
print(f'✓ GitHub token: {os.getenv(\"GITHUB_TOKEN\")[:10]}...')
if os.getenv('NOTION_TOKEN'):
    print(f'✓ Notion token: {os.getenv(\"NOTION_TOKEN\")[:10]}...')
else:
    print('ℹ Notion token not set (optional)')
"
```

## Step 7: Test Your Setup

### Test 1: Basic Import Test

```bash
uv run python -c "import deep_agent, e2b; print('✓ Imports successful')"
```

### Test 2: Sandbox Creation Test

```bash
uv run python -c "
from deep_agent import DeepAgentE2B
print('Creating test sandbox...')
with DeepAgentE2B(sandbox_timeout=60) as agent:
    print('✓ Sandbox created successfully')
    print('✓ Agent initialized')
"
```

### Test 3: Simple Task Test

```bash
uv run main.py "List sandbox information and report configured MCP servers"
```

Expected output:
- Sandbox creation messages
- MCP server configuration messages
- Sandbox information (OS, Python version, etc.)
- MCP server status

## Step 8: Run Your First Example

```bash
# Run a simple GitHub example
uv run examples.py github
```

This will:
1. Create a sandbox
2. Connect to GitHub via MCP
3. List your repositories
4. Analyze them
5. Provide a summary

## Troubleshooting Setup Issues

### Issue: "uv: command not found"

**Solution:**
- Ensure `uv` is installed and in your PATH
- Restart your terminal after installation
- On Windows, you may need to restart PowerShell

### Issue: "Python 3.13 not found"

**Solution:**
- Verify Python 3.13+ is installed: `python --version`
- On some systems, use `python3` instead of `python`
- Update `pyproject.toml` if you need to use a different Python version

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Reinstall dependencies
uv sync --reinstall
```

### Issue: "ANTHROPIC_API_KEY must be provided"

**Solution:**
- Verify `.env` file exists in project root
- Check file permissions (should be readable)
- Ensure variable names match exactly (case-sensitive)
- Try loading manually:
  ```bash
  uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
  ```

### Issue: "Sandbox creation failed"

**Solution:**
- Verify E2B API key is correct
- Check your E2B account has credits/quota
- Verify network connectivity
- Check E2B service status

### Issue: "MCP server not responding"

**Solution:**
- Verify GitHub token has correct scopes
- For Notion: ensure pages are shared with integration
- Check token hasn't expired
- Verify tokens are correct in `.env`

## Next Steps

Once setup is complete:

1. **Read the README**: Review the main README.md for usage examples
2. **Try Examples**: Run `uv run examples.py all` to see all capabilities
3. **Explore Deployment**: Check out `deploy.py` for server mode
4. **Customize**: Modify `deep_agent.py` to customize agent behavior

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting-setup-issues) section above
2. Review the main [README.md](README.md)
3. Check [GitHub Issues](https://github.com/e2b-dev/e2b-mcp-py/issues)
4. Review [E2B Documentation](https://e2b.dev/docs)

## Platform-Specific Notes

### Windows

- Use PowerShell for best compatibility
- Path separators: Use forward slashes in Python code, backslashes in PowerShell commands
- Virtual environment activation: `.venv\Scripts\Activate.ps1`

### macOS

- May need to install Xcode Command Line Tools: `xcode-select --install`
- Use `python3` if `python` points to Python 2

### Linux

- May need to install `python3-venv` package
- Use `python3` if `python` points to Python 2

---

Congratulations! Your Deep Agent E2B setup is complete.

