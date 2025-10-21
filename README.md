# E2B MCP Python Demo

A Python demonstration of using [E2B](https://e2b.dev) with GitHub and Notion MCP (Model Context Protocol) servers, similar to the [TypeScript example](https://github.com/e2b-dev/mcp-demo/blob/main/examples/claude-code.ts).

## Overview

This demo shows how to:

- Create an E2B sandbox with MCP server support
- Configure GitHub and Notion MCP servers
- Use Claude CLI within the sandbox to interact with both services
- Automate tasks across GitHub and Notion

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager 
- E2B API key from [e2b.dev/dashboard](https://e2b.dev/dashboard)
- Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
- GitHub Personal Access Token from [github.com/settings/tokens](https://github.com/settings/tokens)
  - Required scopes: `repo`, `read:user`, `read:org`
- Notion Integration Token from [notion.so/profile/integrations](https://www.notion.so/profile/integrations)
  - Remember to share pages/databases with your integration

## Setup

1. **Install uv**
Follow the instructions [here](https://docs.astral.sh/uv/install.sh) to install uv.

2. **Clone the repository**
```bash
git clone https://github.com/e2b-dev/e2b-mcp-py
cd e2b-mcp-py
```

3. **Install dependencies**
```bash
uv sync
```

4. **Set up environment variables**
You can either create a `.env` file in the root of the project or set the environment variables in your shell.

The following keys are required (well in addition to `E2B_API_KEY`)
```
anthropic_api_key = os.environ["ANTHROPIC_API_KEY"]
notion_api_key = os.environ["NOTION_TOKEN"]
github_token = os.environ["GITHUB_TOKEN"]
```



If you don't have a Notion account, you can comment out the Notion-related code in `main.py` and update the prompt accordingly.

In `main.py`, comment out the following lines:
```python
# notion = Notion(internalIntegrationToken=notion_api_key)
```

And remove the `notion=notion` argument from the `McpServer` constructor:
```python
# mcp_servers = McpServer(notion=notion, githubOfficial=github)
mcp_servers = McpServer(githubOfficial=github)
```

And change the `task` variable to something that doesn't involve Notion, for example:
```python
task = "List my top 3 GitHub repositories by stars"
```

## Usage

Run the demo:
```bash
uv run main.py
```

## What It Does

The demo will:

1. Create an E2B sandbox with environment variables configured
2. Install Claude CLI in the sandbox
3. Configure GitHub and Notion MCP servers
4. Execute a sample task that:
   - Lists your GitHub repositories
   - Creates a Notion page summarizing your top 3 repositories by stars

## Customization

You can modify the task in `main.py` (lines 76-80) to perform different operations:

```python
task = """
Your custom task here that uses GitHub and Notion MCP servers
"""
```