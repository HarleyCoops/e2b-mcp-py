"""Helper script to inspect sandbox files and command outputs."""
import sys
from deep_agent import DeepAgentE2B

if len(sys.argv) < 2:
    print("Usage: uv run inspect_sandbox.py <task>")
    print("\nExamples:")
    print('  uv run inspect_sandbox.py "List all Python files in /home/user"')
    print('  uv run inspect_sandbox.py "Read the file audit_repos.py"')
    print('  uv run inspect_sandbox.py "Show the last 50 lines of stdout from running audit_repos.py"')
    sys.exit(1)

task = " ".join(sys.argv[1:])

print(f"Executing: {task}\n")
print("=" * 60)

try:
    with DeepAgentE2B(sandbox_timeout=120) as agent:
        result = agent.invoke(task)
        
        print("\n" + "=" * 60)
        print("RESULT")
        print("=" * 60)
        
        if "messages" in result:
            for msg in result["messages"]:
                if hasattr(msg, "content"):
                    print(msg.content)
                else:
                    print(msg)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

