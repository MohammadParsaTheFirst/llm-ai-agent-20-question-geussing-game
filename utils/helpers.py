from typing import Tuple
from datetime import datetime

def manage_chat_history(chat_history: list, prompt: str, response: str, max_history: int = 3) -> list:
    chat_history.append({
        "user": prompt,
        "assistant": response,
        "timestamp": datetime.now().isoformat()
    })
    
    if len(chat_history) > max_history:
        chat_history.pop(0)
    
    return chat_history
