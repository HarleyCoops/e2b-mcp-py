# Troubleshooting Guide - Deep Agent E2B

## Common Issues and Solutions

### ZeroDivisionError: Division by Zero

**Symptoms:**
```
ZeroDivisionError: division by zero
```

**Cause:**
This occurs when a script tries to compute ratios or percentages with empty datasets. For example:
- `len(flagged_repos) / len(repos)` when `len(repos) == 0`
- GitHub MCP returned zero repositories
- Data was filtered out completely

**Solutions:**

1. **Check GitHub Token Scopes:**
   ```powershell
   # Verify your token has the right scopes
   uv run diagnose_github.py
   ```

2. **Inspect What GitHub Returned:**
   ```powershell
   uv run inspect_sandbox.py "Use GitHub MCP to list my repositories and show the count"
   ```

3. **Check Token Permissions:**
   - Visit https://github.com/settings/tokens
   - Ensure your token has:
     - `repo` scope (for private repos)
     - `read:user` scope
     - `read:org` scope (if querying org repos)

4. **Test GitHub API Directly:**
   ```powershell
   # Replace YOUR_TOKEN with your actual token
   curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user/repos
   ```

5. **Handle Empty Datasets:**
   The agent now includes better error handling. If you encounter this:
   - The agent will detect ZeroDivisionError and provide guidance
   - Re-run with: `uv run main.py "Audit my GitHub repos, but if there are zero repos, report that instead of dividing"`
   - Or manually inspect: `uv run inspect_sandbox.py "Read audit_repos.py and show where the division happens"`

### Empty Repository List

**Symptoms:**
- GitHub MCP calls succeed but return zero repositories
- Scripts fail because they expect data

**Possible Causes:**

1. **Token Scopes Insufficient:**
   - Token only has `public_repo` scope but you only have private repos
   - Need `repo` scope for private repositories

2. **No Repositories:**
   - Account actually has zero repositories
   - All repos are in organizations you don't have access to

3. **Rate Limiting:**
   - GitHub API rate limit exceeded
   - Check: `curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit`

4. **Organization Access:**
   - Trying to access org repos without `read:org` scope
   - Org admin hasn't granted access

**Solutions:**

```powershell
# Diagnostic script
uv run diagnose_github.py

# Check what GitHub actually returns
uv run main.py "Use GitHub MCP to list ALL my repositories, including private ones, and show the raw response"
```

### Authentication Errors

#### E2B Authentication Error

**Symptoms:**
```
E2B authentication failed
invalid x-api-key
```

**Solution:**
- Verify `E2B_API_KEY` in `.env` file
- Check E2B dashboard: https://e2b.dev/dashboard
- Ensure key hasn't expired
- Verify account has credits/quota

#### Anthropic Authentication Error

**Symptoms:**
```
anthropic.AuthenticationError: invalid x-api-key
```

**Solution:**
- Verify `ANTHROPIC_API_KEY` in `.env` file
- Check Anthropic console: https://console.anthropic.com/
- Create new key if expired
- Ensure key starts with `sk-ant-api03-`

#### GitHub Authentication Error

**Symptoms:**
```
GitHub MCP server not responding
401 Unauthorized
```

**Solution:**
- Verify `GITHUB_TOKEN` in `.env` file
- Check token hasn't expired: https://github.com/settings/tokens
- Verify scopes: `repo`, `read:user`, `read:org`
- Regenerate token if needed

### Sandbox Command Failures

**Symptoms:**
- Commands fail with unclear errors
- Scripts crash without helpful messages

**Solutions:**

1. **Inspect Sandbox Files:**
   ```powershell
   uv run inspect_sandbox.py "List all files in /home/user"
   uv run inspect_sandbox.py "Read the file that failed"
   ```

2. **Check Command Output:**
   ```powershell
   uv run inspect_sandbox.py "Show the last 100 lines of output from the failed command"
   ```

3. **Enhanced Error Detection:**
   The `execute_sandbox_command` tool now automatically detects:
   - ZeroDivisionError
   - Empty dataset warnings
   - Provides helpful error messages

### MCP Server Connection Issues

**Symptoms:**
- MCP servers not configured
- "MCP server not responding" errors

**Solutions:**

1. **Verify Tokens:**
   ```powershell
   uv run python check_keys.py  # If you still have this
   ```

2. **Check MCP Configuration:**
   ```powershell
   uv run main.py "List all configured MCP servers and their status"
   ```

3. **Test Individual MCP Servers:**
   ```powershell
   # Test GitHub
   uv run main.py "Use GitHub MCP to get my user information"
   
   # Test Notion
   uv run main.py "Use Notion MCP to search for pages"
   ```

## Diagnostic Tools

### diagnose_github.py
Tests GitHub MCP integration and token scopes:
```powershell
uv run diagnose_github.py
```

### inspect_sandbox.py
Inspect sandbox files and command outputs:
```powershell
uv run inspect_sandbox.py "your inspection task"
```

Examples:
```powershell
uv run inspect_sandbox.py "Read audit_repos.py"
uv run inspect_sandbox.py "Show all Python files in /home/user"
uv run inspect_sandbox.py "List the last 10 commands run"
```

## Best Practices

1. **Always Check for Empty Data:**
   ```python
   if len(data) == 0:
       return {"error": "No data found", "reason": "..."}
   ratio = len(filtered) / len(data) if len(data) > 0 else 0
   ```

2. **Verify API Responses:**
   - Check if API calls returned data
   - Handle empty responses gracefully
   - Report what was found vs. expected

3. **Use Diagnostic Tools:**
   - Run `diagnose_github.py` before complex GitHub tasks
   - Use `inspect_sandbox.py` to debug script issues
   - Check token scopes regularly

4. **Error Handling:**
   - The agent now includes better error detection
   - ZeroDivisionError is automatically detected and explained
   - Empty datasets trigger warnings with guidance

## Getting Help

1. Check this troubleshooting guide
2. Run diagnostic scripts (`diagnose_github.py`, `inspect_sandbox.py`)
3. Review sandbox logs and command outputs
4. Verify all API keys and tokens
5. Check API rate limits and quotas
6. Review the main [README.md](README.md) for usage examples

