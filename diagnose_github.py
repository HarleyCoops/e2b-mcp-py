"""Diagnostic script to check GitHub MCP integration and token scopes."""
import os
from dotenv import load_dotenv
from deep_agent import DeepAgentE2B

load_dotenv()

print("=" * 60)
print("GitHub MCP Integration Diagnostic")
print("=" * 60)

# Check token exists
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    print("[ERROR] GITHUB_TOKEN not set!")
    exit(1)

print(f"[OK] GITHUB_TOKEN is set (starts with: {github_token[:10]}...)")

# Check token format (GitHub supports both classic and fine-grained tokens)
if github_token.startswith('ghp_'):
    print("[OK] Token format: Classic Personal Access Token (ghp_)")
elif github_token.startswith('github_pat_'):
    print("[OK] Token format: Fine-grained Personal Access Token (github_pat_)")
else:
    print("[WARNING] Token format unexpected - should start with 'ghp_' or 'github_pat_'")

print("\n" + "=" * 60)
print("Testing GitHub MCP via E2B Sandbox")
print("=" * 60)

try:
    with DeepAgentE2B(sandbox_timeout=120) as agent:
        print("\n1. Testing GitHub MCP connection...")
        
        # Try to list repos via MCP
        task = """
        Use the GitHub MCP server to list my repositories.
        Return just the count of repositories found and the first 3 repository names.
        If there are any errors, report them clearly.
        """
        
        print("   Executing task...")
        result = agent.invoke(task)
        
        print("\n[SUCCESS] Task completed")
        print("\nResult summary:")
        if "messages" in result:
            for msg in result["messages"][-3:]:  # Show last few messages
                if hasattr(msg, "content"):
                    try:
                        content = str(msg.content)[:500]  # Truncate long output
                        # Handle Unicode for Windows console
                        content = content.encode('ascii', 'replace').decode('ascii')
                        print(f"  {content}")
                    except Exception as e:
                        print(f"  [Message content (encoding issue): {type(msg.content)}]")
        
except Exception as e:
    print(f"\n[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Recommendations")
print("=" * 60)
print("""
If you got zero repos:
1. Verify your GitHub token has these scopes:
   - repo (for private repos)
   - read:user
   - read:org (if querying org repos)

2. Check if you have any repositories:
   - Visit https://github.com/settings/tokens
   - Verify your token is active
   - Test token manually: curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user/repos

3. If token is correct but returns empty:
   - You may only have private repos and need 'repo' scope
   - Or you may need to check a specific organization
""")

