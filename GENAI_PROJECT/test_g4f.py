import g4f
from g4f.client import Client

client = Client()
providers = [g4f.Provider.BlackboxPro, g4f.Provider.DDGS, g4f.Provider.PollinationsAI, g4f.Provider.ApiAirforce]
for p in providers:
    try:
        print(f"Trying {p.__name__}")
        res = client.chat.completions.create(model="gpt-3.5-turbo", provider=p, messages=[{"role":"user", "content":"say Scenario 1"}])
        print(res.choices[0].message.content)
        break
    except Exception as e:
        print(f"Failed {p.__name__} {e}")
