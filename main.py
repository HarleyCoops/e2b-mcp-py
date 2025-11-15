"""
Deep Agent E2B - Main Entry Point

This is the primary entry point for running the Deep Agent with E2B sandbox integration.
"""

import sys
from deep_agent import DeepAgentE2B


def run_interactive():
    """Run the agent in interactive chat mode."""
    print("Deep Agent E2B - Interactive Mode\n")

    with DeepAgentE2B() as agent:
        agent.chat()


def run_task(task: str):
    """Run a single task and exit."""
    print("Deep Agent E2B - Task Mode\n")

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)

        # Print results
        print("\n" + "=" * 80)
        print("RESULTS")
        print("=" * 80)

        if "messages" in result:
            for msg in result["messages"]:
                if hasattr(msg, "content"):
                    # Handle Unicode encoding for Windows console
                    content = str(msg.content)
                    try:
                        print(f"\n{content}")
                    except UnicodeEncodeError:
                        # Strip emojis and non-ASCII characters for Windows console
                        safe_content = content.encode('ascii', 'ignore').decode('ascii')
                        print(f"\n{safe_content}")
                else:
                    print(f"\n{msg}")


def main():
    """Main entry point with CLI argument handling."""
    if len(sys.argv) > 1:
        # Task mode: run with provided task
        task = " ".join(sys.argv[1:])
        run_task(task)
    else:
        # Interactive mode: start chat session
        run_interactive()


if __name__ == "__main__":
    main()
