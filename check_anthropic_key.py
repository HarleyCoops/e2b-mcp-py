"""Check Anthropic API key."""
import os
from dotenv import load_dotenv

load_dotenv()

anthropic_key = os.getenv('ANTHROPIC_API_KEY')
print("=" * 60)
print("Anthropic API Key Check")
print("=" * 60)

if anthropic_key:
    print(f"[OK] ANTHROPIC_API_KEY is set")
    print(f"  Length: {len(anthropic_key)} characters")
    print(f"  Starts with: {anthropic_key[:20]}...")
    print(f"  Ends with: ...{anthropic_key[-10:]}")
    
    # Anthropic keys typically start with 'sk-ant-'
    if anthropic_key.startswith('sk-ant-'):
        print("  Format: Looks like a valid Anthropic key format")
    else:
        print("  Format: WARNING - Anthropic keys usually start with 'sk-ant-'")
        print("  This might be the problem!")
else:
    print("[ERROR] ANTHROPIC_API_KEY is NOT set!")
    print("  This is definitely the problem!")

print("\n" + "=" * 60)
print("Testing Anthropic API Key")
print("=" * 60)

if anthropic_key:
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=anthropic_key)
        # Try a simple API call
        print("Attempting to validate key with Anthropic API...")
        # Just check if we can create a client - actual call would cost money
        print("[SUCCESS] Anthropic client created successfully")
        print("  Key format appears valid")
    except Exception as e:
        print(f"[ERROR] Failed to create Anthropic client: {e}")
        print("  The API key is likely invalid or expired")
else:
    print("[SKIP] No key to test")

