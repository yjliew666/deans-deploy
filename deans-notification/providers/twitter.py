# providers/twitter.py
from typing import Dict, Any
from .base import NotificationProvider
import twitter_client


class TwitterProvider(NotificationProvider):
    """
    Strategy wrapper around twitter_client.py

    Expected payload keys:
    - 'text': the tweet content as a string
    """

    def send(self, payload: Dict[str, Any]) -> bool:
        text = payload.get("text")

        if not text:
            print("TwitterProvider: missing 'text' in payload")
            return False

        try:
            # twitter_client.main expects the tweet text string
            twitter_client.main(text)
            return True
        except Exception as e:
            # Basic error handling so your Strategy never explodes silently
            print("TwitterProvider error:", e)
            return False
