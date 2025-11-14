import os
import dotenv

dotenv.load_dotenv()

from e2b import Sandbox
from e2b.sandbox.mcp import GithubOfficial, Notion, McpServer


def main():
    # Get required environment variables
    anthropic_api_key = os.environ["ANTHROPIC_API_KEY"]
    notion_api_key = os.environ["NOTION_TOKEN"]
    github_token = os.environ["GITHUB_TOKEN"]

    # Create sandbox with MCP servers configured
    notion = Notion(internalIntegrationToken=notion_api_key)
    github = GithubOfficial(githubPersonalAccessToken=github_token)
    mcp_servers = McpServer(notion=notion, githubOfficial=github)

    sandbox = Sandbox.beta_create(
        envs={"ANTHROPIC_API_KEY": anthropic_api_key}, mcp=mcp_servers, timeout=600
    )

    # Get MCP connection details and configure Claude CLI
    mcp_url = sandbox.beta_get_mcp_url()
    mcp_token = sandbox.beta_get_mcp_token()

    result = sandbox.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout=0,
    )
    print(result.stdout)

    list_mcp_result = sandbox.commands.run(
        f"claude mcp list",
        timeout=0,
        envs={"MCP_TIMEOUT": "120000"},
    )

    print(list_mcp_result.stdout)

    # Run task with Claude using MCP servers
    task = """
    Use the GitHub MCP server to list my repositories,
    then use the Notion MCP server to create a page (search for any parent page to attach it to) summarizing
    the top 3 repositories by stars.
    """

    claude_result = sandbox.commands.run(
        f'echo "{task}" | claude -p --dangerously-skip-permissions',
        timeout=0,
        envs={"MCP_TIMEOUT": "120000"},
    )

    print(claude_result.stdout)
    print(claude_result.stderr)


if __name__ == "__main__":
    main()
