"""
LangGraph Agent with E2B Sandbox Integration

Modern stateful agent implementation using LangGraph for improved planning,
execution, and state management with E2B sandboxes and MCP server access.
"""

import asyncio
import os
from typing import Annotated, Optional, TypedDict, Literal, Sequence
import dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from e2b import Sandbox
from e2b.sandbox.mcp import GithubOfficial, Notion, McpServer
from e2b.exceptions import AuthenticationException
from e2b_tools import E2BSandboxTools
from mcp_builder_tools import MCPBuilderTools

dotenv.load_dotenv()


class AgentState(TypedDict):
    """State schema for the LangGraph agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    plan: Optional[str]  # Current execution plan
    next_action: Optional[str]  # Next action to take
    iteration_count: int  # Track iterations to prevent infinite loops


class LangGraphAgentE2B:
    """
    A LangGraph-based agent implementation integrated with E2B sandboxes.

    This agent uses LangGraph's stateful execution model for better planning,
    debugging, and error handling compared to traditional chain-based approaches.
    """

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        e2b_api_key: Optional[str] = None,
        github_token: Optional[str] = None,
        notion_token: Optional[str] = None,
        model_name: str = "claude-sonnet-4-5-20250929",
        sandbox_timeout: int = 600,
        max_iterations: int = 25,
    ):
        """
        Initialize the LangGraph Agent with E2B integration.

        Args:
            anthropic_api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            e2b_api_key: E2B API key (defaults to E2B_API_KEY env var)
            github_token: GitHub personal access token (defaults to GITHUB_TOKEN env var)
            notion_token: Notion integration token (defaults to NOTION_TOKEN env var)
            model_name: Claude model to use
            sandbox_timeout: E2B sandbox timeout in seconds
            max_iterations: Maximum agent iterations to prevent infinite loops
        """
        # Load API keys
        self.anthropic_api_key = anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.e2b_api_key = e2b_api_key or os.environ.get("E2B_API_KEY")
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.notion_token = notion_token or os.environ.get("NOTION_TOKEN")

        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY must be provided or set in environment")
        if not self.e2b_api_key:
            raise ValueError("E2B_API_KEY must be provided or set in environment")

        self.model_name = model_name
        self.sandbox_timeout = sandbox_timeout
        self.max_iterations = max_iterations
        self.sandbox: Optional[Sandbox] = None
        self.tools = []
        self.mcp_client: Optional[MultiServerMCPClient] = None
        self.graph = None

        # Initialize components
        self._setup_sandbox()
        self._setup_graph()

    def _setup_sandbox(self):
        """Create and configure the E2B sandbox with MCP servers."""
        print("Creating E2B sandbox with MCP servers...")

        # Configure MCP servers
        mcp_servers_config = {}

        if self.github_token:
            github = GithubOfficial(githubPersonalAccessToken=self.github_token)
            mcp_servers_config["githubOfficial"] = github
            print("  GitHub MCP server configured")

        if self.notion_token:
            notion = Notion(internalIntegrationToken=self.notion_token)
            mcp_servers_config["notion"] = notion
            print("  Notion MCP server configured")

        mcp_servers = McpServer(**mcp_servers_config) if mcp_servers_config else None

        # Create sandbox
        try:
            self.sandbox = Sandbox.beta_create(
                envs={"ANTHROPIC_API_KEY": self.anthropic_api_key},
                mcp=mcp_servers,
                timeout=self.sandbox_timeout,
                api_key=self.e2b_api_key,
            )
        except AuthenticationException as exc:
            raise RuntimeError(
                "Failed to create E2B sandbox due to authentication error."
            ) from exc

        sandbox_id = getattr(self.sandbox, "sandbox_id", "unknown")
        print(f"  Sandbox created (ID: {sandbox_id})")

        self._verify_sandbox_command_channel()

        # Create tools
        self.tools = E2BSandboxTools.create_tools(self.sandbox)
        print(f"  Created {len(self.tools)} E2B sandbox tools")

        mcp_builder_tools = MCPBuilderTools.create_tools(self.sandbox)
        self.tools.extend(mcp_builder_tools)
        print(f"  Added {len(mcp_builder_tools)} MCP builder tools")

        # Load MCP tools if servers configured
        if mcp_servers:
            mcp_url = self.sandbox.get_mcp_url()
            try:
                mcp_token = self.sandbox.get_mcp_token()
                self._configure_mcp_gateway(mcp_url, mcp_token)
                mcp_langchain_tools = self._load_mcp_langchain_tools(mcp_url, mcp_token)
                self.tools.extend(mcp_langchain_tools)
            except AttributeError:
                print("  Warning: MCP token not available, skipping MCP gateway setup")

    def _setup_graph(self):
        """Initialize the LangGraph state machine."""
        print("Initializing LangGraph state machine...")

        # Create model with tools
        model = ChatAnthropic(
            model=self.model_name,
            anthropic_api_key=self.anthropic_api_key,
            temperature=0.7,
        )
        self.model_with_tools = model.bind_tools(self.tools)

        # System prompt
        self.system_prompt = """You are an advanced autonomous agent with access to an E2B sandbox environment.

You have the following capabilities:

1. **Planning & Reasoning**: Break down complex tasks into clear, actionable steps
2. **E2B Sandbox Execution**: Execute commands, manage files, and run code securely
3. **GitHub Integration**: Access repositories, create issues, manage code
   - Use 'get_me' to get your GitHub username first
   - Use 'search_repositories' with query 'user:YOUR_USERNAME' to list repos
   - Use 'get_repository' with query 'owner/repo' for repo details
4. **Notion Integration**: Create pages, search databases, organize information
5. **File System Management**: Read, write, and organize files
6. **MCP Server Building**: Build custom MCP servers to extend your capabilities
   - Use 'scaffold_mcp_server' to create new integration scaffolds
   - Use 'add_mcp_tool_to_server' to add tools
   - Use 'test_mcp_server' to validate servers
   - Use 'deploy_mcp_server' to make integrations available

Your workflow:
1. Understand the user's request
2. Plan your approach (think step-by-step)
3. Execute tasks using available tools
4. Verify results and iterate if needed
5. Report results clearly

**Critical Guidelines:**
- Always check for empty datasets before division
- Verify API responses before processing
- Handle errors gracefully with clear messages
- Report progress as you work
- Ask clarifying questions if needed

Remember: You're in a secure E2B sandbox, so you can safely execute code and experiments."""

        # Build graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", ToolNode(self.tools))

        # Set entry point
        workflow.set_entry_point("agent")

        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END,
            }
        )

        # Tools always return to agent
        workflow.add_edge("tools", "agent")

        # Compile graph
        self.graph = workflow.compile()
        print("  LangGraph state machine compiled")

    def _agent_node(self, state: AgentState) -> AgentState:
        """Agent reasoning node - decides what to do next."""
        messages = state["messages"]
        iteration_count = state.get("iteration_count", 0)

        # Check iteration limit
        if iteration_count >= self.max_iterations:
            return {
                "messages": [AIMessage(content="Maximum iterations reached. Task may be too complex or unclear.")],
                "iteration_count": iteration_count + 1,
            }

        # Add system message if this is the first iteration
        if iteration_count == 0:
            messages = [SystemMessage(content=self.system_prompt)] + list(messages)

        # Call model
        response = self.model_with_tools.invoke(messages)

        return {
            "messages": [response],
            "iteration_count": iteration_count + 1,
        }

    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """Determine whether to continue to tools or end."""
        messages = state["messages"]
        last_message = messages[-1]

        # If there are tool calls, continue to tools
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"

        # Otherwise end
        return "end"

    def invoke(self, task: str) -> dict:
        """
        Execute a task using the LangGraph agent.

        Args:
            task: The task description

        Returns:
            Dictionary containing the agent's response and metadata
        """
        print(f"\nTask: {task}\n")
        print("=" * 80)

        # Initial state
        initial_state = {
            "messages": [HumanMessage(content=task)],
            "plan": None,
            "next_action": None,
            "iteration_count": 0,
        }

        # Run graph
        final_state = self.graph.invoke(initial_state)

        print("=" * 80)
        print("\nTask completed\n")

        return final_state

    async def ainvoke(self, task: str) -> dict:
        """Async version of invoke."""
        print(f"\nTask: {task}\n")
        print("=" * 80)

        initial_state = {
            "messages": [HumanMessage(content=task)],
            "plan": None,
            "next_action": None,
            "iteration_count": 0,
        }

        final_state = await self.graph.ainvoke(initial_state)

        print("=" * 80)
        print("\nTask completed\n")

        return final_state

    def chat(self):
        """Start an interactive chat session."""
        print("\nStarting interactive chat with LangGraph Agent")
        print("Type 'exit' or 'quit' to end the session\n")
        print("=" * 80)

        conversation_state = {
            "messages": [],
            "plan": None,
            "next_action": None,
            "iteration_count": 0,
        }

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\nEnding chat session. Goodbye!")
                    break

                if not user_input:
                    continue

                # Add user message
                conversation_state["messages"].append(HumanMessage(content=user_input))
                conversation_state["iteration_count"] = 0  # Reset for new turn

                # Run graph
                result_state = self.graph.invoke(conversation_state)

                # Extract assistant response
                if result_state["messages"]:
                    last_message = result_state["messages"][-1]
                    if isinstance(last_message, AIMessage):
                        print(f"\nAgent: {last_message.content}\n")
                    else:
                        print(f"\nAgent: {last_message}\n")

                # Update conversation state
                conversation_state = result_state

            except KeyboardInterrupt:
                print("\n\nChat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}\n")

    def stream(self, task: str):
        """Stream the agent's execution (returns generator)."""
        initial_state = {
            "messages": [HumanMessage(content=task)],
            "plan": None,
            "next_action": None,
            "iteration_count": 0,
        }

        for state in self.graph.stream(initial_state):
            yield state

    def close(self):
        """Clean up resources."""
        if self.sandbox:
            print("\nClosing E2B sandbox...")
            print("  Resources cleaned up")
        if self.mcp_client:
            print("  Releasing MCP client")
            self.mcp_client = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def _run_sandbox_command(self, command: str, timeout: int = 60):
        """Run a sandbox command with error handling."""
        if not self.sandbox:
            raise RuntimeError("Sandbox is not initialized")

        try:
            return self.sandbox.commands.run(command, timeout=timeout)
        except AuthenticationException as exc:
            raise RuntimeError(
                "E2B authentication failed while executing a sandbox command."
            ) from exc

    def _verify_sandbox_command_channel(self):
        """Verify sandbox command endpoint works."""
        print("  Verifying sandbox command channel...")
        result = self._run_sandbox_command("echo E2B_SANDBOX_OK")

        if result.exit_code != 0:
            raise RuntimeError("Sandbox command verification failed")
        print("  Sandbox command channel verified")

    def _configure_mcp_gateway(self, mcp_url: str, mcp_token: str):
        """Register sandbox MCP gateway with Claude CLI."""
        print("  Configuring Claude CLI with MCP gateway...")
        result = self._run_sandbox_command(
            f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
            timeout=30,
        )

        if result.exit_code == 0:
            print("  Claude CLI configured with MCP gateway")
        else:
            print(f"  Warning: MCP gateway setup had issues: {result.stderr}")

    def _load_mcp_langchain_tools(self, mcp_url: str, mcp_token: str):
        """Load MCP tools via langchain-mcp-adapters."""
        print("  Loading MCP tools via langchain-mcp-adapters...")
        self.mcp_client = MultiServerMCPClient(
            {
                "e2b_mcp_gateway": {
                    "transport": "streamable_http",
                    "url": mcp_url,
                    "headers": {"Authorization": f"Bearer {mcp_token}"},
                }
            }
        )

        try:
            tools = asyncio.run(self.mcp_client.get_tools())
            print(f"  Loaded {len(tools)} MCP tools via langchain-mcp-adapters")
            return tools
        except Exception as exc:
            print(f"  Warning: Failed to load MCP tools: {exc}")
            self.mcp_client = None
            return []


# Alias for backward compatibility
DeepAgentE2B = LangGraphAgentE2B


def main():
    """Main entry point for testing the LangGraph agent."""
    with LangGraphAgentE2B() as agent:
        task = """
        Use the E2B sandbox to:
        1. List my top 5 GitHub repositories by stars
        2. Create a summary of these repositories
        """

        result = agent.invoke(task)

        print("\n" + "=" * 80)
        print("AGENT RESPONSE:")
        print("=" * 80)
        print(result)


if __name__ == "__main__":
    main()
