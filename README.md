# Deep Agent E2B

A sophisticated autonomous agent implementation using the [deepagents](https://github.com/langchain-ai/deepagents) framework integrated with [E2B](https://e2b.dev) sandboxes for secure code execution and Model Context Protocol (MCP) server access.

## 🌟 Features

### Deep Agent Capabilities
- **🧠 Planning & Task Decomposition**: Automatically breaks complex tasks into manageable steps
- **📁 File System Management**: Smart context management through file operations
- **🤖 Subagent Spawning**: Delegates specialized tasks to focused subagents
- **💾 Long-term Memory**: Persistent memory across conversation threads via LangGraph Store
- **🔧 Custom Tools**: Extensive E2B sandbox integration tools

### E2B Integration
- **🔒 Secure Sandbox Execution**: Run code safely in isolated cloud environments
- **🐙 GitHub MCP Server**: Access repositories, create issues, manage code
- **📝 Notion MCP Server**: Create pages, search databases, organize information
- **⚡ Real-time Command Execution**: Execute shell commands and scripts
- **📦 Package Management**: Install and test Python packages dynamically

## 🎯 What Makes This Special?

This project combines the power of **deepagents** (inspired by Claude Code) with **E2B's sandbox technology**, creating an agent that can:

1. **Plan autonomously** using todo lists and task decomposition
2. **Execute code safely** in isolated cloud sandboxes
3. **Access multiple services** (GitHub, Notion) through MCP servers
4. **Manage complex workflows** across platforms
5. **Maintain context** through intelligent file system usage

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **[uv](https://docs.astral.sh/uv/)** package manager
- **API Keys**:
  - [E2B API Key](https://e2b.dev/dashboard) - for sandboxes
  - [Anthropic API Key](https://console.anthropic.com/) - for Claude
  - [GitHub Token](https://github.com/settings/tokens) - with `repo`, `read:user`, `read:org` scopes
  - [Notion Integration Token](https://www.notion.so/profile/integrations) - optional

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/e2b-dev/e2b-mcp-py
   cd e2b-mcp-py
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**

   Create a `.env` file:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-...
   E2B_API_KEY=your_e2b_key
   GITHUB_TOKEN=ghp_...
   NOTION_TOKEN=secret_...  # Optional
   ```

### Basic Usage

#### Interactive Mode

Start a chat session with the agent:

```bash
uv run main.py
```

#### Single Task Mode

Run a specific task:

```bash
uv run main.py "List my top 5 GitHub repos and create a Notion page summarizing them"
```

#### Example Tasks

Run pre-built examples:

```bash
# GitHub repository analysis
uv run examples.py github

# Notion organization
uv run examples.py notion

# GitHub to Notion sync
uv run examples.py sync

# Code execution in sandbox
uv run examples.py code

# Data processing
uv run examples.py data

# Package testing
uv run examples.py package

# Complex multi-step workflow
uv run examples.py workflow

# Run all examples
uv run examples.py all
```

## 🏗️ Architecture

### Project Structure

```
e2b-mcp-py/
├── deep_agent.py      # Core Deep Agent implementation
├── e2b_tools.py       # E2B sandbox tools for LangChain
├── main.py            # Main entry point (interactive & task modes)
├── examples.py        # Pre-built example tasks
├── deploy.py          # Deployment & server mode script
├── legacy_main.py     # Original simple implementation
├── pyproject.toml     # Dependencies and project config
└── README.md          # This file
```

### Component Overview

#### 1. Deep Agent (`deep_agent.py`)

The core autonomous agent with:
- **Initialization**: Sets up E2B sandbox with MCP servers
- **Tool Integration**: Provides 8+ custom E2B tools
- **Task Execution**: Handles single tasks or interactive chat
- **Context Management**: Uses deepagents middleware for planning and file operations

#### 2. E2B Tools (`e2b_tools.py`)

Custom LangChain tools for sandbox interaction:

| Tool | Description |
|------|-------------|
| `execute_sandbox_command` | Run shell commands in the sandbox |
| `read_sandbox_file` | Read files from sandbox filesystem |
| `write_sandbox_file` | Write files to sandbox filesystem |
| `list_sandbox_directory` | List directory contents |
| `execute_github_mcp_action` | Interact with GitHub via MCP |
| `execute_notion_mcp_action` | Interact with Notion via MCP |
| `install_sandbox_package` | Install Python/system packages |
| `get_sandbox_info` | Get sandbox environment details |

#### 3. Main Entry (`main.py`)

Two operation modes:
- **Interactive**: Chat with the agent continuously
- **Task**: Execute a single task and exit

#### 4. Examples (`examples.py`)

Pre-built tasks demonstrating:
- GitHub repository analysis
- Notion page creation
- Cross-platform synchronization
- Code execution and testing
- Data processing workflows
- Multi-step complex operations

#### 5. Deployment (`deploy.py`)

Server-mode capabilities:
- **Persistent Service**: Run as a background server
- **Task Queue**: Process tasks from a queue file
- **Logging**: Comprehensive task logging
- **Auto-retry**: Automatic retry on failures

## 📖 Usage Examples

### Example 1: GitHub Repository Analysis

```python
from deep_agent import DeepAgentE2B

with DeepAgentE2B() as agent:
    result = agent.invoke("""
        Analyze my GitHub repositories:
        1. List all repositories
        2. Identify top 5 by stars
        3. Analyze primary languages used
        4. Create a summary report
    """)
```

### Example 2: Automated Documentation

```python
task = """
For each of my GitHub repositories:
1. Check if README.md exists
2. If missing, generate a basic README template
3. Create a Notion page tracking which repos need documentation
4. Include next steps for manual completion
"""

with DeepAgentE2B() as agent:
    agent.invoke(task)
```

### Example 3: Data Processing

```python
task = """
In the E2B sandbox:
1. Create a Python script that fetches data from a public API
2. Process and analyze the data
3. Generate visualization code (matplotlib)
4. Save results to files
5. Provide a summary of findings
"""

with DeepAgentE2B() as agent:
    agent.invoke(task)
```

### Example 4: Interactive Development

```python
from deep_agent import DeepAgentE2B

with DeepAgentE2B() as agent:
    agent.chat()  # Start interactive session
```

Then in the chat:
```
You: Create a Flask app in the sandbox and test it

Agent: [Plans the task, creates files, installs Flask, writes code, tests it]

You: Now add an endpoint that returns JSON data

Agent: [Modifies the app, adds endpoint, tests it]
```

## 🖥️ Server Deployment

### Running as a Persistent Service

```bash
# Start the server (polls for tasks every 10 seconds)
uv run deploy.py server
```

### Adding Tasks to Queue

```bash
# Add a task to the queue
uv run deploy.py queue "Analyze my GitHub activity from the last week"

# Add another task
uv run deploy.py queue "Create a Notion page with my project status"
```

### Running Single Tasks

```bash
# Execute a task immediately and exit
uv run deploy.py task "List my GitHub repositories"
```

### Task Queue Format

Tasks are stored in `/tmp/deep_agent_queue.json`:

```json
[
  {
    "id": "task_1699564321",
    "description": "Analyze my GitHub activity",
    "metadata": {
      "priority": "high",
      "created_at": "2024-11-14T10:00:00Z"
    }
  }
]
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | ✅ Yes |
| `E2B_API_KEY` | E2B API key for sandboxes | ✅ Yes |
| `GITHUB_TOKEN` | GitHub PAT with repo access | ⚠️ Recommended |
| `NOTION_TOKEN` | Notion integration token | ❌ Optional |

### Custom Configuration

Modify `deep_agent.py` initialization:

```python
agent = DeepAgentE2B(
    model_name="claude-sonnet-4-5-20250929",  # Claude model
    sandbox_timeout=600,  # Sandbox lifetime in seconds
)
```

### Adding Custom Tools

Add your own tools in `e2b_tools.py`:

```python
@tool
def my_custom_tool(parameter: str) -> str:
    """Description of what this tool does."""
    # Your implementation
    return result
```

## 🎓 How It Works

### 1. Initialization Flow

```
User starts agent
    ↓
Create E2B sandbox with MCP servers
    ↓
Configure Claude CLI in sandbox
    ↓
Create E2B tools for LangChain
    ↓
Initialize deepagents with tools
    ↓
Ready to receive tasks
```

### 2. Task Execution Flow

```
User provides task
    ↓
Agent creates plan (write_todos)
    ↓
Agent executes steps using tools
    ↓
Tools interact with E2B sandbox
    ↓
Sandbox executes commands/accesses MCP servers
    ↓
Results returned to agent
    ↓
Agent synthesizes and reports results
```

### 3. Tool Architecture

```
Deep Agent (Python process)
    ↓
LangChain Tools (e2b_tools.py)
    ↓
E2B SDK (e2b.Sandbox)
    ↓
E2B Cloud Sandbox
    ├── Shell Commands
    ├── File System
    ├── Claude CLI
    └── MCP Servers
        ├── GitHub Official
        └── Notion
```

## 🧪 Testing

### Manual Testing

```bash
# Test basic functionality
uv run main.py "List sandbox information"

# Test GitHub integration
uv run main.py "List my GitHub repositories"

# Test Notion integration
uv run main.py "Search for Notion pages"

# Test code execution
uv run examples.py code
```

### Debugging

Enable verbose output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from deep_agent import DeepAgentE2B
# ... rest of your code
```

## 🚨 Troubleshooting

### Common Issues

**1. Sandbox Timeout**
```
Error: Sandbox timed out
```
**Solution**: Increase timeout in initialization:
```python
DeepAgentE2B(sandbox_timeout=1200)  # 20 minutes
```

**2. MCP Server Connection**
```
Error: MCP server not responding
```
**Solution**: Check tokens and permissions:
- GitHub: Ensure token has `repo`, `read:user`, `read:org` scopes
- Notion: Ensure pages are shared with your integration

**3. Missing Dependencies**
```
ModuleNotFoundError: No module named 'deepagents'
```
**Solution**: Run `uv sync` to install all dependencies

**4. API Rate Limits**
- GitHub: 5,000 requests/hour for authenticated requests
- Notion: 3 requests/second
- Anthropic: Based on your tier

## 🔐 Security Considerations

- **Sandbox Isolation**: All code execution happens in isolated E2B sandboxes
- **Token Security**: Never commit `.env` files; use environment variables
- **MCP Permissions**: Grant minimum required permissions to GitHub/Notion tokens
- **Timeout Limits**: Set appropriate timeouts to prevent runaway processes

## 📚 Resources

- [Deepagents Documentation](https://docs.langchain.com/oss/python/deepagents/overview)
- [E2B Documentation](https://e2b.dev/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional MCP server integrations
- More example tasks and workflows
- Enhanced error handling and retry logic
- Web UI for agent interaction
- Metrics and monitoring

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **[LangChain AI](https://github.com/langchain-ai)** for the deepagents framework
- **[E2B](https://e2b.dev)** for sandbox infrastructure
- **[Anthropic](https://anthropic.com)** for Claude
- Inspired by [Claude Code](https://claude.ai/code)

---

Built with ❤️ using Deep Agents + E2B
