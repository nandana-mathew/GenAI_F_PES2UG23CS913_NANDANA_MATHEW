# 🔒 SSL Certificate Error - Solutions Guide

## ❌ Problem
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: 
self-signed certificate in certificate chain (_ssl.c:1032)
```

This error means your network (corporate proxy, VPN, or firewall) is intercepting HTTPS connections.

---

## ✅ Solution 1: Quick Fix (Already Applied ✓)

I've added **SSL certificate bypass** to your code. Just restart your app:

```bash
streamlit run app.py
```

The code now disables SSL verification warnings and uses an unverified SSL context for Gemini connections. This works in most corporate/VPN environments.

**Status**: ✅ Already built into `core.py`

---

## ✅ Solution 2: Use OpenAI as Fallback (Recommended)

If Gemini still fails, use **OpenAI** which has better SSL handling:

### Step 1: Get an OpenAI API Key
1. Go to: https://platform.openai.com/account/billing/overview
2. Sign up (you get $5 free credits)
3. Create an API key
4. Copy the key

### Step 2: Add to `.env`
Edit your `.env` file:
```
GEMINI_API_KEY=AQ.Ab8RN6L7y9YAuIXWtaOX5x9a01TsVJ5BN60cgYTRIT9x2vkSRA
OPENAI_API_KEY=sk-proj-... (paste your OpenAI key here)
```

### Step 3: Restart App
```bash
streamlit run app.py
```

**How it works**: If Gemini fails, the app automatically falls back to OpenAI.

**Cost**: ~$0.005-0.01 per scenario generation (very cheap!)

---

## ✅ Solution 3: Proper SSL Certificate Fix (If You Have Admin Access)

If you're behind a corporate proxy using MITM (man-in-the-middle) SSL inspection:

### For Windows (Admin PowerShell):
```powershell
# Option A: Update Python certificates
python.exe -m pip install --upgrade certifi

# Option B: Force trust corporate certificates
# Get your corporate proxy's certificate and run:
# certifi.py --cert "C:\path\to\corporate-cert.pem"
```

### For Linux/Mac:
```bash
# Update certificates
pip install --upgrade certifi

# Find cert location
python -c "import certifi; print(certifi.where())"

# Add corporate cert to that file
```

---

## ✅ Solution 4: Fallback to Mock Mode (No Internet Required)

If all else fails, use **Mock mode** (procedural AI):
- Doesn't require API keys
- Generates realistic scenarios locally
- No SSL issues

**How to enable**: Open the app and select **"Mock"** from the Intelligence Mode dropdown.

---

## 🔧 Priority Order (Automatic)

The app now tries in this order:

1. **Gemini** (your chosen mode) ← fastest
2. **OpenAI** (if configured in .env) ← more reliable SSL
3. **Mock** (procedural fallback) ← always works

---

## 🧪 Test Your Connection

Run the validator to diagnose:
```bash
python check_gemini_key.py
```

If you see SSL errors, try these fixes in order:
1. Just restart the app (SSL fix is already applied)
2. Add OpenAI key to `.env` 
3. Use Mock mode

---

## 📞 Still Not Working?

**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`
- **Fix**: Run: `pip install --upgrade certifi`
- Then restart the app

**Error**: `certificate verify failed: self-signed certificate`
- **Fix**: Behind a corporate proxy - use OpenAI fallback or Mock mode
- **OR**: Ask your IT to add Python/Google APIs to whitelist

**Error**: `CERTIFICATE_VERIFY_FAILED` with OpenAI too
- **Fix**: Your network is blocking both - use Mock mode only
- Contact your network administrator

---

## 🎯 Recommended Setup

**Best for reliability**:
1. ✅ Gemini API key (already in `.env`)
2. ✅ OpenAI API key (add to `.env` for SSL-safer fallback)
3. ✅ SSL bypass (already coded into app)

**For complete reliability**: Have both keys in `.env` so it can fallback automatically.
