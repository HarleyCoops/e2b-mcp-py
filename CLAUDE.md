# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python demonstration of E2B sandboxes integrated with MCP (Model Context Protocol) servers. The architecture creates a remote sandbox environment where Claude CLI runs with access to configured MCP servers (GitHub and Notion).

**Key architectural pattern**: The code doesn't run Claude locally - it creates an E2B sandbox, configures MCP servers within that sandbox, and then runs Claude CLI commands inside the sandbox. The MCP servers are exposed to Claude via E2B's MCP gateway with token-based authentication.

## Development Commands

This project uses **uv** (not pip) for package management:

```bash
# Install dependencies
uv sync

# Run the main demo
uv run main.py
```

## Environment Variables

Required environment variables (set in `.env` or shell):
- `E2B_API_KEY` - From e2b.dev/dashboard
- `ANTHROPIC_API_KEY` - From console.anthropic.com
- `GITHUB_TOKEN` - Personal access token with `repo`, `read:user`, `read:org` scopes
- `NOTION_TOKEN` - Integration token (only if using Notion functionality)

The `.env` file should never be committed (it's gitignored).

## Code Structure

The entire demo is contained in [main.py](main.py), which follows this flow:

1. **Load environment variables** (lines 1-15)
2. **Configure MCP servers** - Creates `Notion` and `GithubOfficial` server instances with credentials (lines 17-20)
3. **Create E2B sandbox** - Uses `Sandbox.beta_create()` with MCP servers and Anthropic API key passed as envs (lines 22-24)
4. **Configure Claude CLI in sandbox** - Retrieves MCP gateway URL and token, then runs `claude mcp add` command inside the sandbox (lines 26-34)
5. **Execute task** - Writes task to file in sandbox and pipes it to `claude` command with `--dangerously-skip-permissions` flag (lines 44-78)

## Important Implementation Details

### Sandbox Command Execution
- Commands run in the sandbox use `sandbox.commands.run()` with `timeout=0` (no timeout)
- Set `MCP_TIMEOUT` environment variable to `120000` (2 minutes) for MCP operations
- Use `sandbox.files.write()` to write content to files in the sandbox rather than heredoc/echo

### MCP Server Configuration
- MCP servers are configured using E2B's built-in classes: `GithubOfficial`, `Notion`
- The `McpServer` wrapper combines multiple MCP servers
- MCP access is authenticated via bearer token retrieved from `sandbox.beta_get_mcp_token()`

### Error Handling
- Catch `CommandExitException` from e2b.sandbox.commands.command_handle for command failures
- This exception may contain stdout/stderr in various attributes depending on E2B SDK version

## Modifying the Task

To change what Claude does, modify the `task` string variable (around line 45). The task can use any tools provided by the configured MCP servers (GitHub and Notion operations).

To disable Notion: Comment out the Notion server creation (line 18) and remove `notion=notion` from `McpServer()` (line 20).
