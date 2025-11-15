"""
Deployment Script for Deep Agent E2B

This script handles deployment and server-mode operation of the Deep Agent.
It can run as a persistent service, handling tasks from a queue or API.
"""

import os
import time
import json
from typing import Optional, Dict, Any
from pathlib import Path
from deep_agent import DeepAgentE2B


class DeepAgentServer:
    """
    Server-mode wrapper for Deep Agent E2B.

    This class enables running the agent as a persistent service that can:
    - Process tasks from a queue
    - Handle multiple requests sequentially
    - Maintain logs and state
    - Auto-restart on failures
    """

    def __init__(
        self,
        log_dir: str = "/tmp/deep_agent_logs",
        task_queue_file: str = "/tmp/deep_agent_queue.json",
        max_retries: int = 3,
    ):
        """
        Initialize the Deep Agent server.

        Args:
            log_dir: Directory for storing logs
            task_queue_file: Path to task queue file
            max_retries: Maximum retry attempts for failed tasks
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        self.task_queue_file = Path(task_queue_file)
        self.max_retries = max_retries
        self.agent: Optional[DeepAgentE2B] = None

        print(f"Log directory: {self.log_dir}")
        print(f"Task queue file: {self.task_queue_file}")

    def initialize_agent(self):
        """Initialize or reinitialize the agent."""
        print("Initializing agent...")
        try:
            self.agent = DeepAgentE2B()
            print("Agent initialized successfully")
            return True
        except Exception as e:
            print(f"Failed to initialize agent: {str(e)}")
            return False

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single task.

        Args:
            task: Task dictionary with 'id', 'description', and optional 'metadata'

        Returns:
            Result dictionary with status and output
        """
        task_id = task.get("id", "unknown")
        description = task.get("description", "")

        print(f"\n{'=' * 80}")
        print(f"Processing Task: {task_id}")
        print(f"Description: {description}")
        print("=" * 80)

        log_file = self.log_dir / f"task_{task_id}_{int(time.time())}.log"

        try:
            # Ensure agent is initialized
            if not self.agent:
                if not self.initialize_agent():
                    raise Exception("Failed to initialize agent")

            # Execute task
            result = self.agent.invoke(description)

            # Log results
            with open(log_file, "w") as f:
                json.dump(
                    {
                        "task_id": task_id,
                        "description": description,
                        "status": "success",
                        "result": str(result),
                        "timestamp": time.time(),
                    },
                    f,
                    indent=2,
                )

            print(f"Task {task_id} completed successfully")
            print(f"Log saved to: {log_file}")

            return {
                "task_id": task_id,
                "status": "success",
                "result": result,
                "log_file": str(log_file),
            }

        except Exception as e:
            error_msg = str(e)
            print(f"Task {task_id} failed: {error_msg}")

            # Log error
            with open(log_file, "w") as f:
                json.dump(
                    {
                        "task_id": task_id,
                        "description": description,
                        "status": "error",
                        "error": error_msg,
                        "timestamp": time.time(),
                    },
                    f,
                    indent=2,
                )

            return {
                "task_id": task_id,
                "status": "error",
                "error": error_msg,
                "log_file": str(log_file),
            }

    def load_task_queue(self) -> list:
        """Load tasks from the queue file."""
        if not self.task_queue_file.exists():
            return []

        try:
            with open(self.task_queue_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading task queue: {str(e)}")
            return []

    def save_task_queue(self, tasks: list):
        """Save tasks to the queue file."""
        try:
            with open(self.task_queue_file, "w") as f:
                json.dump(tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving task queue: {str(e)}")

    def run_server(self, poll_interval: int = 10):
        """
        Run the server in continuous mode.

        Args:
            poll_interval: Seconds between queue checks
        """
        print("\nStarting Deep Agent Server")
        print(f"Poll interval: {poll_interval} seconds")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                # Load tasks from queue
                tasks = self.load_task_queue()

                if tasks:
                    print(f"Found {len(tasks)} task(s) in queue")

                    # Process first task
                    task = tasks.pop(0)
                    self.process_task(task)

                    # Save updated queue
                    self.save_task_queue(tasks)

                    # Brief pause between tasks
                    time.sleep(2)
                else:
                    # No tasks, wait before checking again
                    print(f"No tasks in queue. Checking again in {poll_interval}s...")
                    time.sleep(poll_interval)

        except KeyboardInterrupt:
            print("\n\nServer stopped by user")
        except Exception as e:
            print(f"\n\nServer error: {str(e)}")
        finally:
            if self.agent:
                self.agent.close()

    def run_single_task(self, description: str, task_id: Optional[str] = None):
        """
        Run a single task immediately.

        Args:
            description: Task description
            task_id: Optional task ID (auto-generated if not provided)
        """
        if not task_id:
            task_id = f"task_{int(time.time())}"

        task = {"id": task_id, "description": description}

        try:
            self.initialize_agent()
            result = self.process_task(task)
            return result
        finally:
            if self.agent:
                self.agent.close()


def deploy_server():
    """Deploy the agent in server mode."""
    server = DeepAgentServer()
    server.run_server(poll_interval=10)


def deploy_single_task(task_description: str):
    """Deploy a single task and exit."""
    server = DeepAgentServer()
    result = server.run_single_task(task_description)

    print("\n" + "=" * 80)
    print("TASK RESULT")
    print("=" * 80)
    print(json.dumps(result, indent=2))


def add_task_to_queue(task_description: str, task_id: Optional[str] = None):
    """Add a task to the queue for later processing."""
    queue_file = Path("/tmp/deep_agent_queue.json")

    # Load existing queue
    if queue_file.exists():
        with open(queue_file, "r") as f:
            tasks = json.load(f)
    else:
        tasks = []

    # Add new task
    if not task_id:
        task_id = f"task_{int(time.time())}"

    tasks.append({"id": task_id, "description": task_description})

    # Save queue
    with open(queue_file, "w") as f:
        json.dump(tasks, f, indent=2)

    print(f"Task {task_id} added to queue")
    print(f"Queue now contains {len(tasks)} task(s)")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python deploy.py server              # Run in server mode")
        print("  python deploy.py task '<description>' # Run single task")
        print("  python deploy.py queue '<description>' # Add task to queue")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "server":
        deploy_server()
    elif mode == "task" and len(sys.argv) > 2:
        task_desc = " ".join(sys.argv[2:])
        deploy_single_task(task_desc)
    elif mode == "queue" and len(sys.argv) > 2:
        task_desc = " ".join(sys.argv[2:])
        add_task_to_queue(task_desc)
    else:
        print("Invalid usage. See help above.")
        sys.exit(1)
