"""Test GitHub repo listing and commit access."""
import json
from deep_agent import DeepAgentE2B

print("=" * 60)
print("GitHub Repository Access Test")
print("=" * 60)

try:
    with DeepAgentE2B(sandbox_timeout=120) as agent:
        # Test: List repos and get commit from first repo
        print("\nTesting: List repos and get most recent commit from first repo...")
        
        task = """
        Use GitHub MCP to:
        1. List my repositories using the list_repos action
        2. Show the exact count of repositories returned
        3. If repos exist, get the most recent commit from the FIRST repository
        4. Show the commit SHA, message, author, and date
        5. If no repos returned, explain why (empty list, error, etc.)
        """
        
        result = agent.invoke(task)
        
        # Extract and print key info
        print("\n" + "=" * 60)
        print("RESULT SUMMARY")
        print("=" * 60)
        
        if "messages" in result:
            for msg in result["messages"]:
                if hasattr(msg, "content"):
                    content = str(msg.content)
                    # Print without special characters that cause encoding issues
                    safe_content = content.encode('ascii', 'ignore').decode('ascii')
                    if len(safe_content) > 0:
                        print(safe_content[:1000])  # First 1000 chars
                        if len(safe_content) > 1000:
                            print("... (truncated)")
        
except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()

