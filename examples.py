"""
Example Tasks for Deep Agent E2B

This module contains example tasks demonstrating the capabilities of the Deep Agent
with E2B sandbox integration.
"""

from deep_agent import DeepAgentE2B


def example_github_analysis():
    """Example: Analyze GitHub repositories."""
    task = """
    Analyze my GitHub repositories and provide insights:
    1. List all my repositories
    2. Identify the top 5 by stars
    3. Analyze the primary languages used across all repos
    4. Create a summary report
    """

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_notion_organization():
    """Example: Organize information in Notion."""
    task = """
    Help me organize my development workflow in Notion:
    1. Search for existing pages related to "projects" or "development"
    2. Create a new page titled "Development Tracker [Auto-generated]"
    3. Add a section listing potential project ideas
    """

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_github_to_notion():
    """Example: Sync GitHub repos to Notion."""
    task = """
    Synchronize GitHub repository information to Notion:
    1. Get my top 5 GitHub repositories by stars
    2. For each repository, extract:
       - Name and description
       - Star count and fork count
       - Primary language
       - Last update date
    3. Create a Notion page titled "Top GitHub Projects [Auto-generated]"
    4. Format the information as a clean, organized page with sections for each repo
    """

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_code_execution():
    """Example: Execute code in the E2B sandbox."""
    task = """
    Create and execute a Python script in the E2B sandbox:
    1. Write a Python script that analyzes system information
    2. The script should gather: OS version, Python version, available disk space
    3. Execute the script in the sandbox
    4. Return the results in a formatted report
    """

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_data_processing():
    """Example: Process data using the sandbox."""
    task = """
    Perform data processing in the E2B sandbox:
    1. Create a sample dataset (CSV file) with mock user data
    2. Write a Python script to analyze the data
    3. Calculate statistics (mean, median, counts)
    4. Generate a summary report
    5. Save both the data and report to files in the sandbox
    """

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_package_testing():
    """Example: Test installing and using packages."""
    task = """
    Test Python package installation and usage:
    1. Install the 'requests' package in the sandbox
    2. Write a script that makes a simple API call to httpbin.org/json
    3. Parse the JSON response
    4. Display the results
    """

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def example_multi_step_workflow():
    """Example: Complex multi-step workflow."""
    task = """
    Execute a complex multi-step development workflow:

    STEP 1 - Repository Analysis:
    - List my GitHub repositories
    - Identify repos that need documentation updates (look for missing READMEs)

    STEP 2 - Documentation Generation:
    - For the first repo without a README, analyze its structure
    - Generate a basic README template with:
      * Project title
      * Description placeholder
      * Installation section
      * Usage section
      * License section

    STEP 3 - Notion Documentation:
    - Create a Notion page titled "Documentation Improvement Plan"
    - List the repositories that need documentation
    - Include the generated README template

    STEP 4 - Summary Report:
    - Create a summary of actions taken
    - List next steps for manual completion
    """

    with DeepAgentE2B() as agent:
        result = agent.invoke(task)
        return result


def run_all_examples():
    """Run all example tasks sequentially."""
    examples = [
        ("GitHub Analysis", example_github_analysis),
        ("Notion Organization", example_notion_organization),
        ("GitHub to Notion Sync", example_github_to_notion),
        ("Code Execution", example_code_execution),
        ("Data Processing", example_data_processing),
        ("Package Testing", example_package_testing),
        ("Multi-Step Workflow", example_multi_step_workflow),
    ]

    print("🚀 Running all example tasks...\n")

    for name, example_func in examples:
        print(f"\n{'=' * 80}")
        print(f"Running: {name}")
        print("=" * 80)

        try:
            example_func()
            print(f"\n✅ {name} completed successfully")
        except Exception as e:
            print(f"\n❌ {name} failed: {str(e)}")

        print("\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        example_name = sys.argv[1].lower()
        examples_map = {
            "github": example_github_analysis,
            "notion": example_notion_organization,
            "sync": example_github_to_notion,
            "code": example_code_execution,
            "data": example_data_processing,
            "package": example_package_testing,
            "workflow": example_multi_step_workflow,
            "all": run_all_examples,
        }

        if example_name in examples_map:
            examples_map[example_name]()
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available examples: {', '.join(examples_map.keys())}")
    else:
        # Run a default example
        example_github_to_notion()
