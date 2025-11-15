"""Test GitHub MCP access - check what we can actually access."""
from deep_agent import DeepAgentE2B

print("=" * 60)
print("GitHub Access Test")
print("=" * 60)

try:
    with DeepAgentE2B(sandbox_timeout=800) as agent:
        # Test 1: Get user info
        print("\n1. Testing GitHub user access...")
        result1 = agent.invoke("Use GitHub MCP to get my GitHub username and user information. Return the raw response.")
        print("Result:", result1)
        
        # Test 2: List repos - get exact count
        print("\n2. Testing repository listing...")
        result2 = agent.invoke("""
        Use GitHub MCP to list my repositories. 
        Return:
        1. The exact count of repositories returned
        2. The first 5 repository names (if any)
        3. Whether the list is empty and why
        4. Any error messages from GitHub MCP
        """)
        print("Result:", result2)
        
        # Test 3: Try to get a specific repo's latest commit
        print("\n3. Testing repository commit access...")
        result3 = agent.invoke("""
        Use GitHub MCP to:
        1. List my repositories
        2. Pick the first repository from the list
        3. Get the most recent commit from that repository
        4. Show the commit SHA, message, and author
        If there are no repositories, report that clearly.
        """)
        print("Result:", result3)
        
except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()

