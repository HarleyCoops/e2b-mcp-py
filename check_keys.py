"""
Quick diagnostics script for verifying Deep Agent E2B credentials.

Run:
    uv run python check_keys.py

The script checks for required environment variables, attempts to create a
temporary sandbox, and runs a simple command to ensure the command channel
does not raise an "invalid x-api-key" (401) error.
"""

from __future__ import annotations

import os
import sys
from contextlib import suppress
from typing import Dict

import dotenv
from e2b import Sandbox
from e2b.exceptions import AuthenticationException, SandboxException

REQUIRED_VARS = ("ANTHROPIC_API_KEY", "E2B_API_KEY")
OPTIONAL_VARS = ("GITHUB_TOKEN", "NOTION_TOKEN")


def mask(value: str | None) -> str:
    if not value:
        return "<missing>"
    if len(value) <= 8:
        return f"{value[0]}***{value[-1]}"
    return f"{value[:4]}...{value[-4:]}"


def print_env_summary() -> Dict[str, str | None]:
    dotenv.load_dotenv()
    print("Credential summary:")

    values: Dict[str, str | None] = {}
    for env_name in (*REQUIRED_VARS, *OPTIONAL_VARS):
        env_value = os.environ.get(env_name)
        values[env_name] = env_value
        label = "required" if env_name in REQUIRED_VARS else "optional"
        status = "present" if env_value else "missing"
        print(f"  - {env_name} ({label}): {status} {mask(env_value)}")

    return values


def main() -> int:
    values = print_env_summary()

    missing = [name for name in REQUIRED_VARS if not values.get(name)]
    if missing:
        print(f"\nMissing required variables: {', '.join(missing)}")
        return 1

    print("\nCreating verification sandbox...")
    try:
        sandbox = Sandbox.beta_create(
            envs={"ANTHROPIC_API_KEY": values["ANTHROPIC_API_KEY"] or ""},
            timeout=60,
            auto_pause=True,
            api_key=values["E2B_API_KEY"],
        )
    except AuthenticationException as exc:
        print(
            "ERROR: Failed to create sandbox due to E2B authentication error. "
            "Double-check E2B_API_KEY in .env."
        )
        print(f"Details: {exc}")
        return 2
    except SandboxException as exc:
        print("ERROR: Sandbox creation failed due to a sandbox error.")
        print(f"Details: {exc}")
        return 2

    print(f"Sandbox created: {sandbox.sandbox_id}")

    print("Running command-channel health check...")
    try:
        result = sandbox.commands.run("echo CHECK_SANDBOX", timeout=30)
    except AuthenticationException as exc:
        print(
            "ERROR: Sandbox command channel rejected the API key (invalid x-api-key). "
            "Update the E2B_API_KEY and re-run this script."
        )
        print(f"Details: {exc}")
        return 3
    except SandboxException as exc:
        print("ERROR: Sandbox command failed.")
        print(f"Details: {exc}")
        return 3
    else:
        if result.exit_code == 0:
            print("Command channel looks healthy.")
        else:
            print(
                f"WARNING: Command channel returned exit code {result.exit_code}. "
                "Check sandbox stdout/stderr for details."
            )
            print(result.stderr)
    finally:
        with suppress(Exception):
            sandbox.kill()

    print("\nDiagnostics complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
