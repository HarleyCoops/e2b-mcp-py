"""Test E2B API key validity."""
import os
from dotenv import load_dotenv

load_dotenv()

e2b_key = os.getenv('E2B_API_KEY')

if not e2b_key:
    print("ERROR: E2B_API_KEY not set!")
    exit(1)

print(f"Testing E2B API key: {e2b_key[:15]}...")
print("\nAttempting to create a test sandbox...")

try:
    from e2b import Sandbox
    
    # Try to create a sandbox with a short timeout
    print("Creating sandbox (this will fail if key is invalid)...")
    sandbox = Sandbox.beta_create(timeout=30)
    print(f"[SUCCESS] Sandbox created! ID: {sandbox.sandbox_id}")
    print("Your E2B API key is valid!")
    sandbox.close()
except Exception as e:
    error_str = str(e)
    print(f"\n[ERROR] Failed to create sandbox:")
    print(f"  Error: {error_str}")
    
    if "401" in error_str or "authentication" in error_str.lower() or "invalid" in error_str.lower():
        print("\n" + "="*60)
        print("DIAGNOSIS: Your E2B API key is INVALID or EXPIRED")
        print("="*60)
        print("\nTo fix this:")
        print("1. Visit https://e2b.dev/dashboard")
        print("2. Go to API Keys section")
        print("3. Create a new API key or check if your key is still active")
        print("4. Update your .env file with the new key")
        print("\nYour current key (first 20 chars):", e2b_key[:20])
    else:
        print("\nThis might be a different issue (network, quota, etc.)")
        print("Check the error message above for details")

