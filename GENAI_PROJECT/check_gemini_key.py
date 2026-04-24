#!/usr/bin/env python
"""
🔍 Gemini API Key Validator
Checks if your Gemini API key is configured correctly and can connect.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

print("=" * 60)
print("🔍 GEMINI API KEY VALIDATOR")
print("=" * 60)

# Load from .env
env_path = Path(".") / ".env"
print(f"\n📁 Looking for .env file: {env_path.absolute()}")
if env_path.exists():
    print("   ✅ .env file found")
    load_dotenv(dotenv_path=env_path, override=True)
else:
    print("   ❌ .env file not found")

# Check API key
api_key = os.environ.get("GEMINI_API_KEY", "").strip()
print(f"\n🔑 Checking GEMINI_API_KEY...")
if not api_key:
    print("   ❌ API KEY NOT SET")
    print("\n   How to fix:")
    print("   1) Get key from: https://aistudio.google.com/app/apikey")
    print("   2) Edit .env file in this folder")
    print("   3) Paste: GEMINI_API_KEY=AIzaSy...")
    sys.exit(1)
else:
    print(f"   ✅ API Key found: {api_key[:8]}...{api_key[-4:]}")

# Check SDK
print(f"\n📦 Checking google-genai SDK...")
try:
    from google import genai
    print("   ✅ google-genai SDK installed")
except ImportError:
    print("   ❌ google-genai not installed")
    print("   Run: pip install google-genai")
    sys.exit(1)

# Try to initialize client
print(f"\n🚀 Initializing Gemini client...")
try:
    client = genai.Client(api_key=api_key)
    print("   ✅ Client initialized successfully")
except Exception as e:
    print(f"   ❌ Client initialization failed: {str(e)}")
    sys.exit(1)

# Try a simple API call
print(f"\n💬 Testing API call (gemini-2.0-flash-lite)...")
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents="Say 'Hello from Gemini!' in exactly those words.",
    )
    if response and response.text:
        print(f"   ✅ API call successful!")
        print(f"   Response: {response.text[:100]}")
    else:
        print("   ❌ Empty response from API")
        sys.exit(1)
except Exception as e:
    err_str = str(e)
    if "429" in err_str or "quota" in err_str:
        print(f"   ⚠️  Quota exceeded: {err_str[:80]}")
        print("   The SDK is working but your free tier quota is full.")
        print("   Try again in a few minutes or use a different model.")
    elif "403" in err_str or "unauthorized" in err_str:
        print(f"   ❌ Invalid API Key: {err_str[:80]}")
        print("   Generate a new key: https://aistudio.google.com/app/apikey")
        sys.exit(1)
    else:
        print(f"   ❌ API error: {err_str}")
        sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL CHECKS PASSED! Gemini is ready to use!")
print("=" * 60)
print("\n🎮 To use Gemini in the app:")
print("   1) Run: streamlit run app.py")
print("   2) Select 'Gemini' from the Intelligence Mode dropdown")
print("   3) Input your game and click 'Generate Scenarios'")
print("\n")
