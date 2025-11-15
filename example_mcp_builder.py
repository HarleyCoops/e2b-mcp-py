"""
MCP Builder Example - JSONPlaceholder API

This example demonstrates the agent's ability to build custom MCP servers.
The agent will create an MCP server for the JSONPlaceholder API autonomously.
"""

from deep_agent import DeepAgentE2B


def example_build_jsonplaceholder_mcp():
    """
    Example: Agent builds an MCP server for JSONPlaceholder API.

    This demonstrates the full workflow:
    1. Scaffold MCP server
    2. Add tools for API endpoints
    3. Test the MCP server
    4. Deploy it
    5. Use the new tools
    """
    task = """
Build a custom MCP server for the JSONPlaceholder API and demonstrate using it.

STEP 1 - SCAFFOLD:
Create an MCP server named 'jsonplaceholder' for the API at https://jsonplaceholder.typicode.com

STEP 2 - ADD TOOLS:
Add the following tools to the MCP server:

Tool 1: get_posts
- Description: "Fetch all posts from JSONPlaceholder"
- Parameters: {"type": "object", "properties": {"limit": {"type": "integer", "description": "Max posts to return"}}, "required": []}
- Implementation:
```python
import httpx
limit = arguments.get("limit", 10)
async with httpx.AsyncClient() as client:
    response = await client.get("https://jsonplaceholder.typicode.com/posts")
    posts = response.json()[:limit]
    return [TextContent(type="text", text=f"Retrieved {len(posts)} posts: {posts}")]
```

Tool 2: get_post
- Description: "Fetch a specific post by ID"
- Parameters: {"type": "object", "properties": {"post_id": {"type": "integer", "description": "Post ID"}}, "required": ["post_id"]}
- Implementation:
```python
import httpx
post_id = arguments.get("post_id")
async with httpx.AsyncClient() as client:
    response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    post = response.json()
    return [TextContent(type="text", text=f"Post {post_id}: {post}")]
```

Tool 3: get_user
- Description: "Fetch user information by ID"
- Parameters: {"type": "object", "properties": {"user_id": {"type": "integer", "description": "User ID"}}, "required": ["user_id"]}
- Implementation:
```python
import httpx
user_id = arguments.get("user_id")
async with httpx.AsyncClient() as client:
    response = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    user = response.json()
    return [TextContent(type="text", text=f"User {user_id}: {user}")]
```

STEP 3 - TEST:
Test the MCP server by calling 'get_posts' with limit=3

STEP 4 - DEPLOY:
Deploy the MCP server in local mode

STEP 5 - LIST:
Use list_mcp_servers to confirm the server is available

STEP 6 - REPORT:
Provide a summary of what was built and how to use it.
"""

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_build_simple_calculator_mcp():
    """
    Example: Agent builds a simple calculator MCP server.

    This is a simpler example that doesn't require external APIs.
    """
    task = """
Build a simple calculator MCP server with basic math operations.

1. Scaffold an MCP server named 'calculator'
2. Add tools: add, subtract, multiply, divide
3. Test with sample calculations
4. Deploy the server
5. Demonstrate using it for: 15 + 27, 100 / 4

Each tool should accept parameters 'a' and 'b' (both numbers).
"""

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_extend_with_custom_api():
    """
    Example: Agent builds MCP server for a custom/internal API.

    This demonstrates how the agent can integrate ANY API.
    """
    task = """
Imagine we have an internal API at https://api.example.com with these endpoints:

GET /health - Health check
GET /metrics - Get system metrics
POST /tasks - Create a new task

Build an MCP server that wraps this API (note: the API doesn't exist,
so the implementation can be mock/placeholder code with comments explaining
what it would do in production).

Include proper error handling and authentication placeholder.
"""

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_list_and_inspect():
    """
    Example: List all built MCP servers and inspect them.
    """
    task = """
1. List all MCP servers that have been built
2. For each server, read its README.md and server.py files
3. Create a summary report of available integrations
"""

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


if __name__ == "__main__":
    import sys

    examples = {
        "jsonplaceholder": example_build_jsonplaceholder_mcp,
        "calculator": example_build_simple_calculator_mcp,
        "custom": example_extend_with_custom_api,
        "list": example_list_and_inspect,
    }

    if len(sys.argv) > 1:
        example_name = sys.argv[1].lower()
        if example_name in examples:
            print(f"\nRunning MCP Builder Example: {example_name}\n")
            print("=" * 80)
            examples[example_name]()
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available examples: {', '.join(examples.keys())}")
    else:
        # Run default example
        print("\nRunning Default MCP Builder Example: JSONPlaceholder\n")
        print("=" * 80)
        example_build_jsonplaceholder_mcp()
