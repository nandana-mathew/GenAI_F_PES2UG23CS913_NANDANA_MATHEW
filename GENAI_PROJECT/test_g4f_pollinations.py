import g4f
from g4f.client import Client

client = Client()
try:
    print(f"Trying PollinationsAI with search model limit")
    res = client.chat.completions.create(model="", provider=g4f.Provider.PollinationsAI, messages=[{"role":"user", "content":"say Scenario 1: Hello"}])
    print("SUCCESS Pollinations:", res.choices[0].message.content)
except Exception as e:
    print(f"Failed PollinationsAI {e}")
