"""
MCP Builder Tools for Deep Agents

This module provides LangChain-compatible tools for building, testing, and deploying
custom MCP servers, enabling the agent to extend its own capabilities.
"""

from langchain_core.tools import tool
from e2b import Sandbox
from typing import Optional
import json


class MCPBuilderTools:
    """
    Wrapper class for MCP server building operations that can be used as LangChain tools.
    """

    def __init__(self, sandbox: Sandbox):
        """
        Initialize MCP builder tools.

        Args:
            sandbox: An active E2B sandbox instance
        """
        self.sandbox = sandbox

    @staticmethod
    def create_tools(sandbox: Sandbox) -> list:
        """
        Create a list of LangChain tools for MCP server building operations.

        Args:
            sandbox: An active E2B sandbox instance

        Returns:
            List of LangChain tools
        """
        tools_instance = MCPBuilderTools(sandbox)

        @tool
        def scaffold_mcp_server(
            server_name: str,
            description: str,
            api_base_url: Optional[str] = None,
        ) -> dict:
            """
            Create a new MCP server scaffold with basic structure.

            This creates a complete MCP server template ready for adding custom tools.
            The server will be created in /home/user/mcp_servers/{server_name}/

            Args:
                server_name: Name of the MCP server (e.g., 'slack', 'stripe', 'jsonplaceholder')
                description: Brief description of what this MCP server does
                api_base_url: Optional base URL for the API this server wraps (e.g., 'https://api.slack.com')

            Returns:
                Dictionary with server_path, files_created, and next_steps
            """
            server_path = f"/home/user/mcp_servers/{server_name}"

            # Create directory structure
            tools_instance.sandbox.commands.run(
                f"mkdir -p {server_path}", timeout=10
            )

            # Generate API configuration section
            api_config = ""
            if api_base_url:
                api_config = f'''# API configuration
API_BASE_URL = "{api_base_url}"
API_TOKEN = os.environ.get("{server_name.upper()}_API_TOKEN", "")
'''

            httpx_import = "import httpx" if api_base_url else ""

            # Generate server.py template
            server_template = f'''"""
{description}

Auto-generated MCP server for {server_name}.
"""

import asyncio
import os
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
{httpx_import}

# Initialize MCP server
server = Server("{server_name}")

{api_config}
# Tool implementations will be added below
# Use @server.list_tools() and @server.call_tool() decorators

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        # Tools will be added here
        Tool(
            name="example_tool",
            description="Example tool - replace with actual implementation",
            inputSchema={{
                "type": "object",
                "properties": {{
                    "param": {{
                        "type": "string",
                        "description": "Example parameter"
                    }}
                }},
                "required": ["param"]
            }}
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "example_tool":
        param = arguments.get("param", "")
        return [TextContent(
            type="text",
            text=f"Example response for: {{param}}"
        )]
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {{name}}"
        )]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
'''

            # Write server file
            tools_instance.sandbox.files.write(
                f"{server_path}/server.py", server_template
            )

            # Create README
            readme_template = f'''# {server_name} MCP Server

{description}

## Setup

```bash
# Install dependencies
pip install mcp httpx

# Run the server
python server.py
```

## Configuration

{f"Set environment variable: `{server_name.upper()}_API_TOKEN`" if api_base_url else "No configuration needed yet."}

## Available Tools

- `example_tool` - Replace with actual tools

## Next Steps

1. Implement actual tools in server.py
2. Test with `test_mcp_server` tool
3. Deploy with `deploy_mcp_server` tool
'''

            tools_instance.sandbox.files.write(
                f"{server_path}/README.md", readme_template
            )

            return {
                "status": "success",
                "server_name": server_name,
                "server_path": server_path,
                "files_created": ["server.py", "README.md"],
                "next_steps": [
                    f"Add tools to {server_path}/server.py",
                    "Test with test_mcp_server",
                    "Deploy with deploy_mcp_server",
                ],
            }

        @tool
        def add_mcp_tool_to_server(
            server_name: str,
            tool_name: str,
            tool_description: str,
            parameters_schema: dict,
            implementation_code: str,
        ) -> dict:
            """
            Add a new tool to an existing MCP server.

            Args:
                server_name: Name of the MCP server (must exist from scaffold_mcp_server)
                tool_name: Name of the tool to add (e.g., 'send_message', 'create_issue')
                tool_description: Description of what the tool does
                parameters_schema: JSON schema for tool parameters (dict with 'properties' and 'required')
                implementation_code: Python code that implements the tool (should return list[TextContent])

            Returns:
                Dictionary with status and updated file path
            """
            server_path = f"/home/user/mcp_servers/{server_name}"

            # Read current server file
            result = tools_instance.sandbox.commands.run(
                f"cat {server_path}/server.py", timeout=10
            )

            if result.exit_code != 0:
                return {
                    "status": "error",
                    "error": f"Server {server_name} not found at {server_path}",
                }

            current_code = result.stdout

            # Generate tool definition
            tool_def = f'''
        Tool(
            name="{tool_name}",
            description="{tool_description}",
            inputSchema={json.dumps(parameters_schema, indent=16)}
        ),'''

            # Generate tool implementation with proper indentation
            # First, normalize the implementation code by removing common leading whitespace
            impl_lines = implementation_code.split("\n")
            # Filter out empty lines for finding minimum indentation
            non_empty_lines = [line for line in impl_lines if line.strip()]
            if non_empty_lines:
                # Find minimum indentation
                min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
                # Remove that baseline indentation and add our target indentation (8 spaces)
                indented_impl = "\n".join(
                    "        " + line[min_indent:] if line.strip() else ""
                    for line in impl_lines
                )
            else:
                indented_impl = ""

            tool_impl = f'''
    if name == "{tool_name}":
        # {tool_description}
{indented_impl}
'''

            # Insert tool definition into list_tools
            updated_code = current_code.replace(
                "# Tools will be added here", f"# Tools will be added here\n{tool_def}"
            )

            # Insert tool implementation into call_tool
            updated_code = updated_code.replace(
                'return [TextContent(\n            type="text",\n            text=f"Unknown tool: {name}"\n        )]',
                f'{tool_impl}\n    \n    return [TextContent(\n            type="text",\n            text=f"Unknown tool: {{name}}"\n        )]',
            )

            # Write updated server file
            tools_instance.sandbox.files.write(
                f"{server_path}/server.py", updated_code
            )

            return {
                "status": "success",
                "server_name": server_name,
                "tool_name": tool_name,
                "message": f"Tool '{tool_name}' added to {server_name} MCP server",
                "server_path": f"{server_path}/server.py",
            }

        @tool
        def test_mcp_server(server_name: str, test_tool: str, test_args: dict) -> dict:
            """
            Test an MCP server by validating its syntax and structure.

            This validates that the server file exists, has valid Python syntax,
            and contains the expected tools. Full runtime testing would require
            MCP SDK installation in the sandbox.

            Args:
                server_name: Name of the MCP server to test
                test_tool: Name of the tool to verify exists in the server
                test_args: Arguments for the tool (currently unused, reserved for future runtime testing)

            Returns:
                Dictionary with test results including syntax validation and tool count
            """
            server_path = f"/home/user/mcp_servers/{server_name}"

            # Check if server exists
            check_result = tools_instance.sandbox.commands.run(
                f"test -f {server_path}/server.py && echo 'exists' || echo 'not found'",
                timeout=5,
            )

            if "not found" in check_result.stdout:
                return {
                    "status": "error",
                    "error": f"Server {server_name} not found at {server_path}",
                }

            # Test Python syntax (validates the file can be compiled)
            syntax_result = tools_instance.sandbox.commands.run(
                f"python3 -m py_compile {server_path}/server.py",
                timeout=10,
            )

            if syntax_result.exit_code != 0:
                return {
                    "status": "error",
                    "server_name": server_name,
                    "error": "Syntax error in server.py",
                    "stderr": syntax_result.stderr,
                }

            # Verify the expected tool exists in the server
            grep_result = tools_instance.sandbox.commands.run(
                f'grep -c \'name="{test_tool}"\' {server_path}/server.py || echo "0"',
                timeout=5,
            )

            tool_found = grep_result.stdout.strip() != "0"

            # Count total tools defined
            tools_count_result = tools_instance.sandbox.commands.run(
                f"grep -c 'Tool(' {server_path}/server.py || echo '0'",
                timeout=5,
            )

            tools_count = int(tools_count_result.stdout.strip() or "0")

            return {
                "status": "success",
                "server_name": server_name,
                "syntax_valid": True,
                "test_tool_found": tool_found,
                "tools_count": tools_count,
                "message": f"Server validated. Found {tools_count} tool(s). Syntax is valid. Tool '{test_tool}' {'found' if tool_found else 'not found'}.",
                "note": "Syntax validation only. Full runtime testing requires MCP SDK in sandbox.",
            }

        @tool
        def deploy_mcp_server(
            server_name: str, deployment_mode: str = "local"
        ) -> dict:
            """
            Deploy an MCP server to make it available to the agent.

            Args:
                server_name: Name of the MCP server to deploy
                deployment_mode: Deployment mode - 'local' (stdio) or 'http' (future)

            Returns:
                Dictionary with deployment status and connection info
            """
            server_path = f"/home/user/mcp_servers/{server_name}"

            if deployment_mode == "local":
                # For local deployment, we create a config entry
                # that can be used with claude mcp add
                config = {
                    "mcpServers": {
                        server_name: {
                            "command": "python",
                            "args": [f"{server_path}/server.py"],
                        }
                    }
                }

                # Save config
                tools_instance.sandbox.files.write(
                    f"{server_path}/mcp_config.json", json.dumps(config, indent=2)
                )

                # Add to Claude CLI (similar to how E2B MCP gateway is added)
                add_result = tools_instance.sandbox.commands.run(
                    f'claude mcp add {server_name} --command python --args "{server_path}/server.py"',
                    timeout=30,
                )

                return {
                    "status": "success" if add_result.exit_code == 0 else "partial",
                    "server_name": server_name,
                    "deployment_mode": "local_stdio",
                    "config_path": f"{server_path}/mcp_config.json",
                    "message": f"MCP server '{server_name}' deployed locally. Tools are now available via Claude CLI.",
                    "stdout": add_result.stdout,
                    "stderr": add_result.stderr,
                }
            else:
                return {
                    "status": "error",
                    "error": f"Deployment mode '{deployment_mode}' not yet implemented",
                }

        @tool
        def list_mcp_servers() -> dict:
            """
            List all MCP servers that have been built.

            Returns:
                Dictionary with list of servers and their details
            """
            result = tools_instance.sandbox.commands.run(
                "ls -la /home/user/mcp_servers/ 2>/dev/null || echo 'No servers found'",
                timeout=10,
            )

            servers = []
            if "No servers found" not in result.stdout:
                lines = result.stdout.strip().split("\n")[3:]  # Skip ., .., total
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 9:
                        server_name = parts[-1]
                        # Read README to get description
                        readme_result = tools_instance.sandbox.commands.run(
                            f"head -n 3 /home/user/mcp_servers/{server_name}/README.md | tail -n 1",
                            timeout=5,
                        )
                        description = (
                            readme_result.stdout.strip()
                            if readme_result.exit_code == 0
                            else "No description"
                        )
                        servers.append(
                            {"name": server_name, "description": description}
                        )

            return {
                "status": "success",
                "count": len(servers),
                "servers": servers,
                "mcp_servers_dir": "/home/user/mcp_servers",
            }

        return [
            scaffold_mcp_server,
            add_mcp_tool_to_server,
            test_mcp_server,
            deploy_mcp_server,
            list_mcp_servers,
        ]
