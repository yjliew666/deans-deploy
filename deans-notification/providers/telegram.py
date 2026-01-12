# providers/telegram.py

from typing import Dict, Any
from .base import NotificationProvider

class TelegramProvider(NotificationProvider):
    def send(self, payload: Dict[str, Any]) -> bool:
        # Demo only: print instead of real API call
        message = payload.get("message", "")
        print("[Mock Telegram] Would send message:", message)
        return True
