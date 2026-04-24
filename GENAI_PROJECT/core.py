import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load env safely
load_dotenv(override=True)

SUPPORTED_GAMES = {
    "rummy": "rummy.txt",              "basic rummy": "rummy.txt",
    "straight rummy": "rummy.txt",
    "gin rummy": "gin_rummy.txt",      "gin": "gin_rummy.txt",
    "indian rummy": "indian_rummy.txt", "paplu": "indian_rummy.txt",
    "13 card rummy": "indian_rummy.txt",
    "canasta": "canasta.txt",
    "kalooki": "kalooki.txt",          "kaluki": "kalooki.txt",
    "caribbean kalooki": "kalooki.txt",
    "contract rummy": "contract_rummy.txt",
    "liverpool rummy": "contract_rummy.txt",
    "shanghai rummy":  "contract_rummy.txt", "may i": "contract_rummy.txt",
    "crazy eights": "crazy_eights.txt",  "crazy 8s": "crazy_eights.txt",
    "switch": "crazy_eights.txt",
}

RULES_DIR = Path("rules")

# Games that use a "Secret Joker" (Wild card rank chosen from deck)
GAMES_WITH_WILD_RANK = ["Indian Rummy", "13 Card Rummy", "Paplu"]

SYSTEM_PROMPT = """
You are an expert Game Strategist AI. Your task is to analyze complex board and card game situations and provide high-level strategic foresight.

STRICT PRINCIPLES:
- GROUNDING: Base reasoning strictly on rules and specific cards.
- PRECISION: MAX 3 scenarios. Each MAX 3 bullets. Each bullet MAX 12 words.
- NO FLUFF: Eliminate theoretical uncertainty. Focus on immediate tactical risk.
- CARD-SPECIFIC: Must mention specific cards in the player's hand.
- NO RECOMMENDATIONS: Describe branches of possibility, not instructions.

TASK:
Identify 3 tactical future scenarios for the next 1-3 turns.

Each scenario MUST include:
1. Description: Punchy bullet on likely opponent intent.
2. Consequences: Short bullet on the immediate board fallout.
3. Tactical Risks: One specific card-based danger to watch for.

UNCERTAINTY USAGE:
Use only: probably, likely, may, could, suggests.

FORMATTING:
You MUST start each scenario with EXACTLY the word 'Scenario' followed by the number, for example:
Scenario 1:
Description: ...
Consequences: ...
Tactical Risks: ...

Scenario 2:
...
"""

VALIDATOR_PROMPT_TEMPLATE = """
You are a Validation Agent. Critically evaluate the generated game scenarios below.

Game Rules:
{rules}

Generated Scenarios:
{scenarios}

For EACH scenario, evaluate these 5 criteria and give PASS or FAIL with a short reason:

1. Rule Compliance     — Does it follow the game rules?
2. Logical Consistency — Are there contradictions?
3. Hidden Info Check   — Does it assume unknown opponent cards?
4. Uncertainty Usage   — Does it use words: may / could / possibly / might / perhaps?
5. Diversity           — Is this scenario clearly different from the other two?

Then give:
OVERALL SUMMARY:
- Total scenarios evaluated: 3
- Valid scenarios (all 5 criteria PASS): X
- Key issues found: ...
- Overall quality rating: [GOOD / ACCEPTABLE / POOR]
"""

MOCK_RESPONSES = {
    "rummy": """Scenario 1:
Description: • Opponent likely building Hearts run after picking 8H.
Consequences: • Hearts card pool thinning; harder for you to meld.
Risks: • Penalty risk from unmelded King of Spades in hand.

Scenario 2:
Description: • Stock empty in <5 turns; transition to endgame.
Consequences: • Players discarding high 'deadwood' cards soon.
Risks: • Getting caught with unmelded face-cards during declaration.

Scenario 3:
Description: • Player 4 likely close to winning; already melded Spades.
Consequences: • Other players dumping cards to minimize final score.
Risks: • Missing own meld opportunity if turn-count miscalculated.
""",
    "canasta": """Scenario 1:
Description: • Opponents took pile; likely holding wild cards (2s/Jokers).
Consequences: • Immediate threat of opponents going out suddenly.
Risks: • Extreme penalty points from unmelded Aces in hand.

Scenario 2:
Description: • Discard pile frozen; forced to draw from thinning stock.
Consequences: • Opportunity to take the pile effectively lost.
Risks: • Partnership stalls before establishing a base canasta.

Scenario 3:
Description: • Partner discarding Diamonds suggests surplus or suit change.
Consequences: • You should hold Diamonds to support their potential meld.
Risks: • Discarding a card partner needed for their second canasta.
""",
    "crazy eights": """Scenario 1:
Description: • Player 4 has 1 card; likely high rank or 8.
Consequences: • Game ends this turn unless suit changes.
Risks: • Absorbing full hand score if no power card held.

Scenario 2:
Description: • Draw-2 penalty pending from Player 4's action.
Consequences: • Hand size will increase, delaying your potential victory.
Risks: • No 2 or 8 in hand to block penalty.

Scenario 3:
Description: • Diamonds suit set; opponents drawing, suggesting they lack it.
Consequences: • Temporary advantage with your current Diamond cards.
Risks: • Next player overrides suit with an 8.
"""
}

MOCK_OUTPUT = MOCK_RESPONSES["rummy"] # Default fallback

# Supported Games Meta (Starts Empty)
DEFAULT_STATES = {k.title(): {"game": k.title(), "num_players": 2, "turn": 1, "player_hand": [], "recent_actions": [], "observations": [], "uncertainty_notes": []} for k in SUPPORTED_GAMES.keys()}


def sort_hand(hand_list: list) -> list:
    """Sorts hand by suit and then rank (ascending)."""
    if not hand_list: return []
    
    suit_order = {"Hearts ♥": 0, "Diamonds ♦": 1, "Clubs ♣": 2, "Spades ♠": 3, "Special": 4}
    rank_order = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11, "Queen": 12, "King": 13, "Ace": 14}
    
    def get_sort_key(card):
        if "Joker" in card: return (4, 99)
        if "Red Three" in card: return (4, 98)
        if " of " not in card: return (4, 97)
        parts = card.split(" of ")
        rank, suit = parts[0], parts[1]
        return (suit_order.get(suit, 4), rank_order.get(rank, 0))
    
    return sorted(hand_list, key=get_sort_key)

def has_national_sequence(hand_list: list) -> bool:
    """Detects if a Pure/National Sequence (3+ consecutive cards, same suit, no Joker) exists."""
    if not hand_list: return False
    
    # 1. Group by Suit
    suits_data = {}
    for card in hand_list:
        if " of " not in card: continue
        parts = card.split(" of ")
        rank, suit = parts[0], parts[1]
        if suit not in suits_data: suits_data[suit] = []
        
        # Rank values (Ace can be 1 or 14)
        r_map = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11, "Queen": 12, "King": 13, "Ace": 14}
        val = r_map.get(rank, 0)
        if val > 0: suits_data[suit].append(val)
        if rank == "Ace": suits_data[suit].append(1) # Add Ace as low too

    # 2. Check for sequences in each suit
    for suit in suits_data:
        vals = sorted(list(set(suits_data[suit])))
        if len(vals) < 3: continue
        
        # Find contiguous chunks
        count = 1
        for i in range(len(vals) - 1):
            if vals[i+1] == vals[i] + 1:
                count += 1
                if count >= 3: return True
            else:
                count = 1
    return False

def load_rules(game_name: str) -> str:
    key = game_name.lower().strip()
    fname = SUPPORTED_GAMES.get(key)
    if not fname:
        # Fallback if no specific rule
        return "Rules not found. Proceed based on general standard mechanics of the game."
    path = RULES_DIR / fname
    if not path.exists():
        return f"Rule file missing: {path}"
    return path.read_text(encoding="utf-8")


def build_context(gs: dict) -> str:
    hand = "\n".join(f"  - {c}" for c in gs["player_hand"])
    acts = "\n".join(f"  • {a}" for a in gs["recent_actions"])
    obs  = "\n".join(f"  • {o}" for o in gs["observations"])
    unc  = "\n".join(f"  • {u}" for u in gs["uncertainty_notes"])
    
    opc_text = f"Top Discard (Open Card): {gs.get('open_card', 'None')}\n" if gs.get('open_card') else ""
    wild_card = gs.get('wild_card', 'None')
    wild_text = f"Game Wild Card (Secret Joker): {wild_card}\n" if wild_card else ""
    
    # Explicitly inform AI about the special rule override
    rule_note = ""
    if wild_card and "Joker" in wild_card:
        rule_note = "NOTE: Since the Secret Joker is a Joker, ACES are considered Wild for this game session.\n"
    
    return (
        f"Game: {gs['game']}\n"
        f"Number of Players: {gs['num_players']}\n"
        f"Turn Number: {gs['turn']}\n\n"
        f"{rule_note}"
        f"My Hand:\n{hand}\n\n"
        + opc_text + wild_text + "\n" +
        f"Recent Public Actions:\n{acts}\n\n"
        f"Observed Behaviour:\n{obs}\n\n"
        f"Uncertainty / Missing Information:\n{unc}"
    )


def create_prompt(game_state: dict, rules: str, context: str) -> str:
    return f"""{SYSTEM_PROMPT}

Game Rules:
{rules}

Current Situation:
{context}
"""


def generate_dynamic_mock(gs: dict) -> str:
    """Generates procedural tactical scenarios based on the actual hand to reduce 'theoretical' feel."""
    game = gs.get("game", "Rummy").title()
    hand = gs.get("player_hand", [])
    open_card = gs.get("open_card", "Unknown")
    wild_card = gs.get("wild_card", "None")
    
    # 1. Analyze hand for specifics
    suits = {}
    for c in hand:
        if " of " in c:
            s = c.split(" of ")[1]
            suits[s] = suits.get(s, 0) + 1
            
    dominant_suit = max(suits, key=suits.get) if suits else "None"
    high_cards = [c for c in hand if any(x in c for x in ["Jack", "Queen", "King", "Ace"])]
    wilds = [c for c in hand if "Joker" in c or "Wild" in c]
    
    # Contextual check
    has_potential_meld = any(count >= 3 for count in suits.values())
    
    # 2. Build Scenarios
    # Scenario 1: Focus on the dominant suit or lack thereof
    if dominant_suit != "None":
        sc1_desc = f"• Opponents likely tracking your interest in {dominant_suit} based on your discards."
        sc1_conseq = f"• Expect resistance or 'blocking' discards in the {dominant_suit} suit."
        sc1_risks = f"• Stall risk for your primary {dominant_suit} sequence; consider pivoting."
    else:
        sc1_desc = "• Scattered hand suggests you are in early-game building phase."
        sc1_conseq = "• High reliance on stock draws to find a matching suit core."
        sc1_risks = "• Inventory risk: Holding too many unrelated suits decreases draw efficiency."

    # Scenario 2: Focus on Penalties/Endgame
    if high_cards:
        sc2_desc = f"• Significant deadwood pressure detected from {len(high_cards)} high-value cards."
        sc2_conseq = "• Sudden declaration by opponent would cause heavy point penalty."
        sc2_risks = f"• Watch for the {high_cards[0].split(' of ')[0]} becoming a liability if stock thins."
    else:
        sc2_desc = f"• Low-point hand strategy provides an 'under-cutting' safety net."
        sc2_conseq = "• You can afford to wait 2-3 more turns for a better stock draw."
        sc2_risks = "• Risk of being outpaced by an opponent building high-value Canastas/Melds."

    # Scenario 3: Focus on Wild Cards and Hidden States
    if wilds:
        sc3_desc = f"• Your {wilds[0]} acts as a tactical anchor for multiple possible melds."
        sc3_conseq = "• Flexibility allows you to wait for the TOP OF DISCARD ({open_card}) to improve."
        sc3_risks = "• Temptation to hold the wild card too long; opponent might go out first."
    else:
        sc3_desc = f"• Hand lacks a Wild Card stabilizer; purely reliant on natural runs."
        sc3_conseq = "• Tactical disadvantage compared to players holding Jokers or 2s."
        sc3_risks = f"• Extremely high risk if the Secret Joker ({wild_card}) is buried in the stock."

    return f"""Scenario 1:
Description: {sc1_desc}
Consequences: {sc1_conseq}
Risks: {sc1_risks}

Scenario 2:
Description: {sc2_desc}
Consequences: {sc2_conseq}
Risks: {sc2_risks}

Scenario 3:
Description: {sc3_desc}
Consequences: {sc3_conseq}
Risks: {sc3_risks}
"""

def get_mock_output(game_name: str, active_state: dict = None) -> str:
    if active_state:
        return generate_dynamic_mock(active_state)
    
    game_key = game_name.lower()
    for key in MOCK_RESPONSES:
        if key in game_key:
            return MOCK_RESPONSES[key]
    return MOCK_RESPONSES["rummy"]

def call_llm(prompt: str, mode: str = "Mock", active_state: dict = None) -> str:
    def fallback_to_mock():
        if active_state:
            return get_mock_output(active_state.get("game", "rummy"), active_state)
        return MOCK_OUTPUT

    if mode == "Mock":
        time.sleep(1.5)
        if "Critically evaluate" in prompt:
            return """1. Rule Compliance: PASS
2. Logical Consistency: PASS
3. Hidden Info Check: PASS
4. Uncertainty Usage: PASS
5. Diversity: PASS

OVERALL: GOOD (High confidence in tactical validity)"""
        if active_state:
            return generate_dynamic_mock(active_state)
        for game in SUPPORTED_GAMES:
            if f"Game: {game.title()}" in prompt:
                return get_mock_output(game)
        return MOCK_OUTPUT

    if mode == "Qwen-2.5":
        try:
            import g4f
            from g4f.client import Client
        except ImportError:
            return "Error: g4f library not found. Run: pip install -U g4f"

        try:
            client = Client()
            messages = [
                {"role": "system", "content": "You are a Game Strategist. Output EXACTLY 3 tactical scenarios. Format each starting EXACTLY with 'Scenario X:'. Keep answers short and strictly grounded in the game."},
                {"role": "user", "content": prompt}
            ]
            
            # List of reliable providers and their required model strings
            providers = [
                (g4f.Provider.PollinationsAI, ""),
                (g4f.Provider.BlackboxPro, "gpt-3.5-turbo"),
                (g4f.Provider.DDGS, "gpt-3.5-turbo"),
                (g4f.Provider.ApiAirforce, "gpt-3.5-turbo")
            ]
            
            last_error = ""
            for provider, model_name in providers:
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        provider=provider,
                        messages=messages
                    )
                    if response and response.choices:
                        return response.choices[0].message.content
                except Exception as e:
                    last_error = f"{provider.__name__ if hasattr(provider, '__name__') else provider}: {e}"
                    continue
                    
            # IF ALL FALLBACKS FAIL DO NOT CRASH: Generate Mock Data instead!
            mock_res = get_mock_output(active_state.get("game", "rummy"), active_state) if active_state else MOCK_OUTPUT
            return mock_res + "\n\n*(Note: Displaying dynamic Mock Scenarios because free AI endpoints are momentarily down. Switch to Gemini in the sidebar for guaranteed 100% uptime).* "
            
        except Exception as e:
            fallback = get_mock_output(active_state.get("game", "rummy"), active_state) if active_state else MOCK_OUTPUT
            return fallback + "\n\n*(Note: G4F threw an exception, showing Mock fallback. Switch to Gemini!)*"

    if mode == "Gemini":
        try:
            from google import genai
        except ImportError:
            return "Error: Please install google-genai library (pip install google-genai)"

        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            return "Error: GEMINI_API_KEY is not set in the .env file."

        try:
            import ssl
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            ssl._create_default_https_context = ssl._create_unverified_context
            client = genai.Client(api_key=api_key)
        except Exception as e:
            return f"Error: Failed to initialize Gemini client: {e}"

        models = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.5-pro"]
        for model_name in models:
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    if response and response.text:
                        return response.text
                    break
                except Exception as e:
                    err_str = str(e).lower()
                    if ("429" in err_str or "quota" in err_str or "exhaust" in err_str):
                        break
                    if ("503" in err_str or "demand" in err_str) and attempt < 1:
                        time.sleep(1.5)
                        continue
                    return f"Error connecting to Gemini {model_name}: {e}"
        return "Error: All Gemini models failed. Check your API key and quota."

    if mode == "Groq":
        try:
            from groq import Groq
        except ImportError:
            return "Error: Please install groq library (pip install groq)"

        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key:
            return "Error: GROQ_API_KEY is not set in the .env file."

        try:
            client = Groq(api_key=api_key)
        except Exception as e:
            return f"Error: Failed to initialize Groq client: {e}"

        models = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"]
        for model_name in models:
            for attempt in range(2):
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    if response and response.choices and response.choices[0].message.content:
                        return response.choices[0].message.content
                    break
                except Exception as e:
                    err_str = str(e).lower()
                    if ("429" in err_str or "quota" in err_str or "exhaust" in err_str):
                        break
                    if ("503" in err_str or "demand" in err_str) and attempt < 1:
                        time.sleep(1.5)
                        continue
                    return f"Error connecting to Groq models: {e}"
        return f"Error: All Groq models failed. Check your API key and connection."

    return fallback_to_mock()


def compute_metrics(scenarios_text: str, validation_text: str) -> dict:
    UNCERTAINTY_WORDS = ["may", "could", "possibly", "might", "perhaps", "unclear", "unknown", "likely", "probably", "suggests", "probability"]
    s = scenarios_text.lower()
    v = validation_text.lower()

    def check(keyword, password="pass"):
        idx = v.find(keyword)
        if idx == -1: return "CHECK REPORT"
        window = v[idx:idx+100]
        return "PASS" if password in window else "CHECK REPORT"

    return {
        "Scenario Count": f"{s.count('scenario')} / 3",
        "Uncertainty Words": f"{sum(s.count(w) for w in UNCERTAINTY_WORDS)} occurrences",
        "Rule Compliance": check("rule compliance"),
        "No Hidden Info": check("hidden info"),
        "Diversity": check("diversity"),
        "Logical Consistency": check("logical consistency"),
        "Format Correct": "PASS" if all(f"scenario {i}" in s for i in ["1", "2", "3"]) else "FAIL",
    }
