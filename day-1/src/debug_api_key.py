import os
from setup import create_gemini_config

def debug_api_setup():
    """
    Debug function to check if API key is properly configured
    """
    print("🔍 Debugging API setup...")

    # Check environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        print("💡 Solution: Check your .env file")
        return False

    print(f"✅ API key found (length: {len(api_key)})")

    # Test configuration creation
    try:
        config, client, model = create_gemini_config()
        print("✅ Configuration created successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False

if __name__ == "__main__":
    debug_api_setup()
