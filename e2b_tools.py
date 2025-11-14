"""
E2B Sandbox Tools for Deep Agents

This module provides LangChain-compatible tools for interacting with E2B sandboxes,
enabling deep agents to execute commands, manage files, and interact with MCP servers.
"""

from typing import Any, Optional
from langchain_core.tools import tool
from e2b import Sandbox


class E2BSandboxTools:
    """
    Wrapper class for E2B sandbox operations that can be used as LangChain tools.
    """

    def __init__(self, sandbox: Sandbox):
        """
        Initialize E2B sandbox tools.

        Args:
            sandbox: An active E2B sandbox instance
        """
        self.sandbox = sandbox

    @staticmethod
    def create_tools(sandbox: Sandbox) -> list:
        """
        Create a list of LangChain tools for E2B sandbox operations.

        Args:
            sandbox: An active E2B sandbox instance

        Returns:
            List of LangChain tools
        """
        tools_instance = E2BSandboxTools(sandbox)

        @tool
        def execute_sandbox_command(command: str, timeout: int = 60) -> dict:
            """
            Execute a shell command in the E2B sandbox.

            Args:
                command: The shell command to execute
                timeout: Timeout in seconds (0 for no timeout)

            Returns:
                Dictionary with stdout, stderr, and exit_code
            """
            result = tools_instance.sandbox.commands.run(command, timeout=timeout)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.exit_code,
            }

        @tool
        def read_sandbox_file(path: str) -> str:
            """
            Read a file from the E2B sandbox filesystem.

            Args:
                path: Absolute path to the file in the sandbox

            Returns:
                File contents as string
            """
            try:
                content = tools_instance.sandbox.files.read(path)
                if isinstance(content, bytes):
                    return content.decode("utf-8")
                return content
            except Exception as e:
                return f"Error reading file: {str(e)}"

        @tool
        def write_sandbox_file(path: str, content: str) -> str:
            """
            Write content to a file in the E2B sandbox filesystem.

            Args:
                path: Absolute path where to write the file
                content: Content to write to the file

            Returns:
                Success message or error
            """
            try:
                tools_instance.sandbox.files.write(path, content)
                return f"Successfully wrote to {path}"
            except Exception as e:
                return f"Error writing file: {str(e)}"

        @tool
        def list_sandbox_directory(path: str = "/home/user") -> list:
            """
            List contents of a directory in the E2B sandbox.

            Args:
                path: Directory path to list (default: /home/user)

            Returns:
                List of file and directory names
            """
            try:
                result = tools_instance.sandbox.commands.run(f"ls -la {path}")
                return result.stdout.split("\n")
            except Exception as e:
                return [f"Error listing directory: {str(e)}"]

        @tool
        def execute_github_mcp_action(action: str, query: str = "") -> dict:
            """
            Execute a GitHub MCP server action through the sandbox.

            This tool interacts with the GitHub MCP server configured in the sandbox
            to perform GitHub operations like listing repos, creating issues, etc.

            Args:
                action: The GitHub action to perform (e.g., 'list_repos', 'get_repo_info')
                query: Additional query parameters or repository name

            Returns:
                Dictionary with action results
            """
            # Use Claude CLI with MCP in the sandbox to execute GitHub actions
            command = f'echo "Use GitHub MCP to {action} {query}" | claude -p --dangerously-skip-permissions'
            result = tools_instance.sandbox.commands.run(
                command, timeout=120, envs={"MCP_TIMEOUT": "120000"}
            )
            return {
                "action": action,
                "query": query,
                "output": result.stdout,
                "error": result.stderr,
            }

        @tool
        def execute_notion_mcp_action(action: str, query: str = "") -> dict:
            """
            Execute a Notion MCP server action through the sandbox.

            This tool interacts with the Notion MCP server configured in the sandbox
            to perform Notion operations like creating pages, searching databases, etc.

            Args:
                action: The Notion action to perform (e.g., 'create_page', 'search')
                query: Additional query parameters or content

            Returns:
                Dictionary with action results
            """
            # Use Claude CLI with MCP in the sandbox to execute Notion actions
            command = f'echo "Use Notion MCP to {action} {query}" | claude -p --dangerously-skip-permissions'
            result = tools_instance.sandbox.commands.run(
                command, timeout=120, envs={"MCP_TIMEOUT": "120000"}
            )
            return {
                "action": action,
                "query": query,
                "output": result.stdout,
                "error": result.stderr,
            }

        @tool
        def install_sandbox_package(package: str, use_pip: bool = True) -> dict:
            """
            Install a Python or system package in the E2B sandbox.

            Args:
                package: Package name to install
                use_pip: If True, use pip; if False, use apt-get

            Returns:
                Installation result
            """
            if use_pip:
                command = f"pip install {package}"
            else:
                command = f"sudo apt-get update && sudo apt-get install -y {package}"

            result = tools_instance.sandbox.commands.run(command, timeout=300)
            return {
                "package": package,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.exit_code,
            }

        @tool
        def get_sandbox_info() -> dict:
            """
            Get information about the E2B sandbox environment.

            Returns:
                Dictionary with sandbox details
            """
            info = {
                "sandbox_id": tools_instance.sandbox.id,
                "template": getattr(
                    tools_instance.sandbox, "template", "default"
                ),
            }

            # Get system information
            result = tools_instance.sandbox.commands.run("uname -a && pwd && whoami")
            info["system_info"] = result.stdout

            return info

        return [
            execute_sandbox_command,
            read_sandbox_file,
            write_sandbox_file,
            list_sandbox_directory,
            execute_github_mcp_action,
            execute_notion_mcp_action,
            install_sandbox_package,
            get_sandbox_info,
        ]
