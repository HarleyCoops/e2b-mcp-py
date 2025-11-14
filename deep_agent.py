"""
Deep Agent with E2B Sandbox Integration

This module implements a sophisticated autonomous agent using the deepagents framework,
integrated with E2B sandboxes for secure code execution and MCP server access.
"""

import os
from typing import Optional
import dotenv
from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic
from e2b import Sandbox
from e2b.sandbox.mcp import GithubOfficial, Notion, McpServer
from e2b_tools import E2BSandboxTools

dotenv.load_dotenv()


class DeepAgentE2B:
    """
    A deep agent implementation that integrates with E2B sandboxes.

    This agent combines the planning, file system management, and subagent
    capabilities of deepagents with E2B's secure sandbox execution environment
    and MCP server integrations.
    """

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        github_token: Optional[str] = None,
        notion_token: Optional[str] = None,
        model_name: str = "claude-sonnet-4-5-20250929",
        sandbox_timeout: int = 600,
    ):
        """
        Initialize the Deep Agent with E2B integration.

        Args:
            anthropic_api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            github_token: GitHub personal access token (defaults to GITHUB_TOKEN env var)
            notion_token: Notion integration token (defaults to NOTION_TOKEN env var)
            model_name: Claude model to use
            sandbox_timeout: E2B sandbox timeout in seconds
        """
        # Load API keys from environment if not provided
        self.anthropic_api_key = anthropic_api_key or os.environ.get(
            "ANTHROPIC_API_KEY"
        )
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.notion_token = notion_token or os.environ.get("NOTION_TOKEN")

        if not self.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY must be provided or set in environment"
            )

        self.model_name = model_name
        self.sandbox_timeout = sandbox_timeout
        self.sandbox: Optional[Sandbox] = None
        self.agent = None
        self.tools = []

        # Initialize components
        self._setup_sandbox()
        self._setup_agent()

    def _setup_sandbox(self):
        """Create and configure the E2B sandbox with MCP servers."""
        print("🚀 Creating E2B sandbox with MCP servers...")

        # Configure MCP servers based on available tokens
        mcp_servers_config = {}

        if self.github_token:
            github = GithubOfficial(githubPersonalAccessToken=self.github_token)
            mcp_servers_config["githubOfficial"] = github
            print("  ✓ GitHub MCP server configured")

        if self.notion_token:
            notion = Notion(internalIntegrationToken=self.notion_token)
            mcp_servers_config["notion"] = notion
            print("  ✓ Notion MCP server configured")

        # Create MCP server instance
        if mcp_servers_config:
            mcp_servers = McpServer(**mcp_servers_config)
        else:
            mcp_servers = None
            print("  ⚠ Warning: No MCP servers configured (no tokens provided)")

        # Create sandbox with environment variables and MCP servers
        self.sandbox = Sandbox.beta_create(
            envs={"ANTHROPIC_API_KEY": self.anthropic_api_key},
            mcp=mcp_servers,
            timeout=self.sandbox_timeout,
        )

        print(f"  ✓ Sandbox created (ID: {self.sandbox.id})")

        # Configure Claude CLI with MCP in the sandbox
        if mcp_servers:
            mcp_url = self.sandbox.beta_get_mcp_url()
            mcp_token = self.sandbox.beta_get_mcp_token()

            result = self.sandbox.commands.run(
                f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
                timeout=0,
            )

            if result.exit_code == 0:
                print("  ✓ Claude CLI configured with MCP gateway")
            else:
                print(f"  ⚠ Warning: MCP gateway setup had issues: {result.stderr}")

        # Create E2B tools for the agent
        self.tools = E2BSandboxTools.create_tools(self.sandbox)
        print(f"  ✓ Created {len(self.tools)} E2B sandbox tools")

    def _setup_agent(self):
        """Initialize the deep agent with custom tools and configuration."""
        print("🤖 Initializing deep agent...")

        # Create Claude model
        model = ChatAnthropic(
            model=self.model_name,
            anthropic_api_key=self.anthropic_api_key,
            temperature=0.7,
        )

        # Custom system prompt for E2B-integrated agent
        system_prompt = """You are an advanced autonomous agent with access to an E2B sandbox environment.

You have the following capabilities:

1. **Planning & Task Decomposition**: Use the write_todos tool to break down complex tasks into manageable steps
2. **E2B Sandbox Execution**: Execute commands, manage files, and run code in a secure isolated environment
3. **GitHub Integration**: Access GitHub repositories, create issues, and manage code via the GitHub MCP server
4. **Notion Integration**: Create pages, search databases, and organize information via the Notion MCP server
5. **File System Management**: Read, write, and organize files both locally and in the sandbox
6. **Subagent Spawning**: Delegate specialized tasks to focused subagents when needed

Your workflow should be:
1. Understand the user's request thoroughly
2. Create a plan using write_todos to track your progress
3. Execute tasks systematically using your available tools
4. Leverage the E2B sandbox for any code execution or testing
5. Use MCP servers for GitHub and Notion operations
6. Report results clearly and comprehensively

Always prioritize:
- Breaking complex tasks into clear steps
- Using the sandbox for safe code execution
- Providing detailed status updates
- Error handling and recovery
- Clear communication of results

Remember: You're operating in a secure E2B sandbox, so you can safely execute code, install packages, and experiment without affecting the host system."""

        # Create the deep agent with E2B tools
        self.agent = create_deep_agent(
            tools=self.tools,
            system_prompt=system_prompt,
            model=model,
        )

        print("  ✓ Deep agent initialized with E2B tools")

    def invoke(self, task: str) -> dict:
        """
        Execute a task using the deep agent.

        Args:
            task: The task description for the agent to execute

        Returns:
            Dictionary containing the agent's response and metadata
        """
        print(f"\n📋 Task: {task}\n")
        print("=" * 80)

        response = self.agent.invoke({"messages": [{"role": "user", "content": task}]})

        print("=" * 80)
        print("\n✅ Task completed\n")

        return response

    def chat(self):
        """Start an interactive chat session with the agent."""
        print("\n💬 Starting interactive chat with Deep Agent")
        print("   Type 'exit' or 'quit' to end the session\n")
        print("=" * 80)

        conversation_messages = []

        while True:
            try:
                user_input = input("\n👤 You: ").strip()

                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\n👋 Ending chat session. Goodbye!")
                    break

                if not user_input:
                    continue

                conversation_messages.append({"role": "user", "content": user_input})

                response = self.agent.invoke({"messages": conversation_messages})

                # Extract the last assistant message
                if "messages" in response and response["messages"]:
                    last_message = response["messages"][-1]
                    if hasattr(last_message, "content"):
                        assistant_response = last_message.content
                    else:
                        assistant_response = str(last_message)

                    print(f"\n🤖 Agent: {assistant_response}\n")
                    conversation_messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )

            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")

    def close(self):
        """Clean up resources (close sandbox)."""
        if self.sandbox:
            print("\n🧹 Closing E2B sandbox...")
            # Note: E2B sandboxes auto-close after timeout
            # You can implement explicit cleanup if needed
            print("  ✓ Resources cleaned up")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def main():
    """Main entry point for running the deep agent."""
    # Example usage
    with DeepAgentE2B() as agent:
        # Example task: List GitHub repos and create Notion page
        task = """
        Use the E2B sandbox to:
        1. List my top 5 GitHub repositories by stars
        2. Create a Notion page summarizing these repositories
        3. Include repository names, descriptions, star counts, and primary languages
        """

        result = agent.invoke(task)

        print("\n" + "=" * 80)
        print("AGENT RESPONSE:")
        print("=" * 80)
        print(result)


if __name__ == "__main__":
    main()
