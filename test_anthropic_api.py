"""Test Anthropic API key with actual API call."""
import os
from dotenv import load_dotenv

load_dotenv()

anthropic_key = os.getenv('ANTHROPIC_API_KEY')

if not anthropic_key:
    print("ERROR: ANTHROPIC_API_KEY not set!")
    exit(1)

print(f"Testing Anthropic API key: {anthropic_key[:20]}...")
print("\nAttempting to make a test API call...")

try:
    from langchain_anthropic import ChatAnthropic
    
    # Create model exactly like the agent does
    model = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        anthropic_api_key=anthropic_key,
        temperature=0.7,
    )
    
    print("Model created successfully")
    print("Making a test API call (this will cost a small amount)...")
    
    # Make a minimal test call
    response = model.invoke("Say 'test' and nothing else.")
    print(f"\n[SUCCESS] API call successful!")
    print(f"Response: {response.content}")
    print("\nYour Anthropic API key is VALID and working!")
    
except Exception as e:
    error_str = str(e)
    print(f"\n[ERROR] API call failed:")
    print(f"  Error type: {type(e).__name__}")
    print(f"  Error message: {error_str}")
    
    if "401" in error_str or "authentication" in error_str.lower() or "invalid" in error_str.lower():
        print("\n" + "="*60)
        print("DIAGNOSIS: Your Anthropic API key is INVALID or EXPIRED")
        print("="*60)
        print("\nTo fix this:")
        print("1. Visit https://console.anthropic.com/")
        print("2. Go to API Keys section")
        print("3. Check if your key is still active")
        print("4. Create a new API key if needed")
        print("5. Update your .env file with the new key")
        print("\nYour current key (first 20 chars):", anthropic_key[:20])
    elif "rate limit" in error_str.lower() or "429" in error_str:
        print("\nThis is a rate limit issue, not an authentication issue.")
        print("Wait a moment and try again.")
    else:
        print("\nThis might be a different issue.")
        print("Check the error message above for details.")

