# providers/facebook.py
from typing import Dict, Any
from .base import NotificationProvider
import facebook_client

class FacebookProvider(NotificationProvider):
    def send(self, payload: Dict[str, Any]) -> bool:
        if "text" not in payload or "deansURL" not in payload:
            print("FacebookProvider: missing 'text' or 'deansURL'")
            return False

        try:
            facebook_client.main(payload)
            return True
        except Exception as e:
            print("FacebookProvider error:", e)
            return False
