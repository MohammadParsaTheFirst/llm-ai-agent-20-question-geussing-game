import requests
from datetime import datetime

class ExaService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.exa.ai/search"
        
        self.SEARCH_KEYWORDS = {
            "current", "now", "today", "recent", "latest", "newest",
            "president", "prime minister", "leader", "ceo", "director",
            "election", "score", "result", "winner", "champion",
            "price", "rate", "stock", "market", "weather",
            "2023", "2024", "2025", "this year", "last month"
        }
    
    def requires_search(self, prompt: str) -> bool:
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in self.SEARCH_KEYWORDS)
    
    def search(self, query: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        current_year = datetime.now().year
        refined_query = f"{query} {current_year}"
        payload = {
            "query": refined_query,
            "numResults": 2,
            "text": True,
            "highlights": False
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            results = response.json().get("results", [])
            if not results:
                return "[No relevant search results found]"
            return "\n".join([f"• {r.get('title', 'Untitled')}: {r.get('text', '')[:300]}" for r in results])
        except requests.exceptions.HTTPError as e:
            return f"[Search error: HTTP {e.response.status_code} - {e.response.text}]"
        except requests.exceptions.RequestException as e:
            return f"[Search error: {str(e)}]"
