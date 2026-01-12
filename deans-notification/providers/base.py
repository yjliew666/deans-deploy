# providers/base.py

from typing import Protocol, Dict, Any

class NotificationProvider(Protocol):
    def send(self, payload: Dict[str, Any]) -> bool:
        """Send a notification. Returns True if success, False otherwise."""
        ...
