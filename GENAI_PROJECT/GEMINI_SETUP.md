# 🚀 Gemini API Setup Guide

## The Issue
Your GenAI project wasn't using Gemini because the **API key was missing or not set properly**.

## Solution (3 Simple Steps)

### Step 1: Get a FREE Gemini API Key
1. Go to: **https://aistudio.google.com/app/apikey**
2. Click "Create API Key"
3. Copy the generated key (starts with `AIzaSy...`)
4. **⚠️ KEEP THIS SECRET - Never share it publicly**

### Step 2: Add Your API Key to `.env`
The `.env` file is ready in your project folder. Open it and paste:
```
GEMINI_API_KEY=AIzaSy... (paste your actual key here)
```

### Step 3: Restart Your Streamlit App
```bash
streamlit run app.py
```

## How to Verify It Works
1. Open the app in your browser
2. On the left sidebar, select **"Gemini"** mode (instead of Mock)
3. Input your game state and click "Generate Scenarios"
4. You should see: ✅ "gemini-2.0-flash | Attempt 1/2..." in the terminal

## Troubleshooting

### "No API Key found" Error
- Make sure `.env` file exists in the project folder
- Check that `GEMINI_API_KEY=AIzaSy...` is on the first uncommented line
- Restart the Streamlit app after editing `.env`

### "403: Invalid API Key" Error
- Double-check you copied the full key correctly
- Go to https://aistudio.google.com/app/apikey and generate a NEW key
- Update your `.env` file

### "429: Quota Exceeded" Error
- Your free tier quota ran out for that model
- The app will automatically rotate to the next available model
- Wait a few minutes and try again
- Or switch to OpenAI mode if you have an API key for that

## Model Rotation
If Gemini rotates through models, here's the priority order:
1. `gemini-2.0-flash` (fastest)
2. `gemini-2.0-flash-lite` (most quota-friendly)
3. `gemini-1.5-flash`
4. `gemini-1.5-flash-8b`
5. `gemini-1.5-pro` (most powerful)

## Features Now Enabled
✅ Real Gemini LLM integration  
✅ Automatic model rotation on quota limits  
✅ Better error messages  
✅ Fallback to OpenAI if configured  
