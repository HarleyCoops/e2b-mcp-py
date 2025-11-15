# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Deep Agent E2B is an autonomous agent stack that combines the **deepagents** planning framework (LangChain) with **E2B sandboxes** and **Model Context Protocol (MCP)** servers. This creates a production-ready system where AI agents can plan complex tasks, execute code securely in isolated sandboxes, and interact with GitHub and Notion via MCP.

**Critical architectural distinction**: This is NOT a simple wrapper around Claude CLI in a sandbox. It's a sophisticated LangChain-based autonomous agent that uses E2B for secure execution and MCP for external integrations.

## Development Commands

This project uses **uv** (not pip) for package management:

```bash
# Install dependencies
uv sync

# Interactive chat mode
uv run main.py

# Single task execution
uv run main.py "<task description>"

# Run example scenarios
uv run examples.py github      # GitHub analysis
uv run examples.py notion      # Notion operations
uv run examples.py sync        # GitHub to Notion sync
uv run examples.py code        # Code execution demo
uv run examples.py data        # Data processing demo
uv run examples.py package     # Package installation demo
uv run examples.py workflow    # Complex multi-step workflow
uv run examples.py all         # Run all examples

# MCP builder examples (self-extending capabilities)
uv run example_mcp_builder.py jsonplaceholder   # Build MCP for JSONPlaceholder API
uv run example_mcp_builder.py calculator        # Build simple calculator MCP
uv run example_mcp_builder.py custom            # Build MCP for custom API
uv run example_mcp_builder.py list              # List all built MCP servers

# Deployment modes
uv run deploy.py task "<task>"         # One-off task with JSON result
uv run deploy.py queue "<task>"        # Add task to queue
uv run deploy.py server                # Long-running worker mode
```

## Environment Variables

Required (all stored in `.env`, which is gitignored):

- `ANTHROPIC_API_KEY` - From console.anthropic.com (used by ChatAnthropic)
- `E2B_API_KEY` - From e2b.dev/dashboard (for sandbox creation)
- `GITHUB_TOKEN` - Personal access token with `repo`, `read:user`, `read:org` scopes (enables GitHub MCP)
- `NOTION_TOKEN` - Integration token (optional, enables Notion MCP)

## Architecture & Code Structure

### Core Components

1. **DeepAgentE2B** ([deep_agent.py](deep_agent.py)) - Main agent class
   - Loads environment variables and API keys
   - Creates E2B sandbox with MCP server configuration
   - Initializes deepagents framework with Claude Sonnet 4.5
   - Wires up E2B tools and MCP tools via langchain-mcp-adapters
   - Provides `invoke(task)` for single tasks and `chat()` for interactive sessions
   - Handles cleanup via context manager protocol

2. **E2BSandboxTools** ([e2b_tools.py](e2b_tools.py)) - LangChain tool implementations
   - `execute_sandbox_command` - Run shell commands in sandbox
   - `read_sandbox_file` / `write_sandbox_file` - File I/O
   - `list_sandbox_directory` - Directory listing
   - `execute_github_mcp_action` - GitHub operations via MCP
   - `execute_notion_mcp_action` - Notion operations via MCP
   - `install_sandbox_package` - Install Python/system packages
   - `get_sandbox_info` - Sandbox environment details
   - All tools wrapped with `_with_auth_guard` for E2B authentication error handling

3. **MCPBuilderTools** ([mcp_builder_tools.py](mcp_builder_tools.py)) - Self-extension capabilities
   - `scaffold_mcp_server` - Create new MCP server scaffold
   - `add_mcp_tool_to_server` - Add tools to existing MCP server
   - `test_mcp_server` - Test MCP server before deployment
   - `deploy_mcp_server` - Deploy and register MCP server
   - `list_mcp_servers` - List all built MCP servers
   - Enables agent to build integrations for any API autonomously

4. **Entry Points**
   - [main.py](main.py) - CLI with interactive chat or single-task modes
   - [examples.py](examples.py) - Curated demo scenarios
   - [deploy.py](deploy.py) - Production deployment with queue and logging

### Execution Flow

1. **Initialization** - `DeepAgentE2B.__init__()` loads secrets, creates E2B sandbox, configures MCP servers (GitHub, Notion)
2. **Tool Wiring** - `E2BSandboxTools.create_tools()` exposes sandbox operations as LangChain tools
3. **MCP Integration** - Uses `langchain-mcp-adapters` `MultiServerMCPClient` to load MCP tools as native LangChain tools
4. **Agent Creation** - `create_deep_agent()` from deepagents framework creates planning-capable agent
5. **Task Execution** - Agent decomposes task, calls tools, iterates until completion
6. **Cleanup** - Sandbox auto-closes after timeout; explicit cleanup via context manager

### Deployment Modes

- **Interactive**: `uv run main.py` - chat loop with conversation history
- **Single Task**: `uv run main.py "task"` - execute once and exit
- **Server Mode**: `uv run deploy.py server` - polls `/tmp/deep_agent_queue.json` every 10s, writes JSON logs to `/tmp/deep_agent_logs/`
- **Queue Producer**: `uv run deploy.py queue "task"` - add task without restarting server

## Important Implementation Details

### GitHub MCP Tool Names

**Critical**: GitHub MCP does NOT have a `list_repos` tool. The agent system prompt in [deep_agent.py:158-161](deep_agent.py#L158-L161) documents the correct pattern:

1. First call `get_me` (no query) to get the username
2. Then call `search_repositories` with query `user:USERNAME` to list repos

Other common GitHub MCP tools:

- `get_repository` - query format: `owner/repo`
- `get_commit` - query format: `owner/repo/commit_sha`
- `list_issues` - query format: `owner/repo`

### Error Handling Patterns

All E2B operations wrapped in `_with_auth_guard` (see [e2b_tools.py:27-38](e2b_tools.py#L27-L38)) to catch `AuthenticationException` and provide clear error messages.

The `execute_sandbox_command` tool has enhanced error detection ([e2b_tools.py:74-90](e2b_tools.py#L74-L90)):

- Detects `ZeroDivisionError` (often from computing ratios with empty datasets)
- Detects empty result patterns and suggests checking MCP permissions/scopes

Agent system prompt includes critical error handling guidelines ([deep_agent.py:180-186](deep_agent.py#L180-L186)):

- Always check for empty datasets before division
- Verify lists are non-empty before computing ratios
- Report empty MCP results clearly rather than proceeding
- Investigate failed API calls (token scopes, permissions, rate limits)

### MCP Configuration

MCP servers configured via E2B's built-in classes ([deep_agent.py:84-96](deep_agent.py#L84-L96)):

```python
github = GithubOfficial(githubPersonalAccessToken=self.github_token)
notion = Notion(internalIntegrationToken=self.notion_token)
mcp_servers = McpServer(githubOfficial=github, notion=notion)
```

MCP tools exposed TWO ways:

1. **Claude CLI in sandbox** - `claude mcp add` with MCP gateway URL and bearer token
2. **LangChain tools** - `MultiServerMCPClient` with `streamable_http` transport ([deep_agent.py:325-356](deep_agent.py#L325-L356))

### Sandbox Command Execution

- Commands use `sandbox.commands.run(command, timeout=seconds)`
- MCP operations should set `timeout=120` and `envs={"MCP_TIMEOUT": "120000"}`
- File writes use `sandbox.files.write(path, content)` - never heredoc/echo
- Sandbox auto-closes after `sandbox_timeout` (default 600s, configurable in constructor)

### Code Style

**No emojis** - per [.github/copilot-instructions.md](.github/copilot-instructions.md), never use emojis in code, comments, or output. This project previously had Unicode encoding issues on Windows (see [main.py:39-41](main.py#L39-L41)).

### MCP Builder Capability (Self-Extension)

**Key innovation**: The agent can build its own MCP servers to integrate with ANY API.

**Workflow for building new integrations:**

1. **Scaffold**: `scaffold_mcp_server(server_name, description, api_base_url)` - Creates template in `/home/user/mcp_servers/{server_name}/`
2. **Implement**: `add_mcp_tool_to_server(server_name, tool_name, description, parameters_schema, implementation_code)` - Adds tools
3. **Test**: `test_mcp_server(server_name, test_tool, test_args)` - Validates server works
4. **Deploy**: `deploy_mcp_server(server_name, deployment_mode)` - Registers with Claude CLI
5. **Use**: New tools immediately available via MCP

**Example use cases:**

- No existing MCP server: Build from scratch (e.g., Stripe, Twilio, internal APIs)
- Existing MCP server: Build custom version with specific tools/workflows
- Composition: Combine multiple APIs into one MCP server
- Customization: Build MCP server aware of your company's schema/fields

**Files created per MCP server:**

```
/home/user/mcp_servers/{server_name}/
  server.py           # MCP server implementation
  README.md           # Documentation
  test_script.py      # Auto-generated tests
  mcp_config.json     # Deployment config
```

**This transforms the agent from:**

- Agent with N pre-configured integrations
- TO: Agent that can integrate with any API on-demand

See [example_mcp_builder.py](example_mcp_builder.py) for demonstrations and [VISION.md](VISION.md) for detailed architecture.

## Modifying Behavior

**Change agent behavior**: Edit system prompt in [deep_agent.py:150-188](deep_agent.py#L150-L188)

**Add new sandbox tools**: Add functions to [e2b_tools.py](e2b_tools.py) decorated with `@tool`, return in `create_tools()`

**Add MCP servers**: Modify `_setup_sandbox()` in [deep_agent.py:77-136](deep_agent.py#L77-L136) to include additional E2B MCP server classes

**Change model**: Pass `model_name="claude-opus-4-20250514"` to `DeepAgentE2B()`

**Increase timeout**: Pass `sandbox_timeout=1200` to `DeepAgentE2B()` (in seconds)

## Troubleshooting

**Sandbox creation fails**: Check `E2B_API_KEY` validity at e2b.dev/dashboard

**MCP authentication errors**: Verify token scopes (GitHub: `repo`, `read:user`, `read:org`; Notion: proper page sharing)

**ZeroDivisionError in tasks**: Usually means MCP returned empty data - check token permissions and retry logic

**Missing dependency**: Run `uv sync` (reads `uv.lock` for reproducible builds)

**Timeout errors**: Increase `sandbox_timeout` when creating `DeepAgentE2B` instance
