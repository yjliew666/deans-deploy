# providers/twilio.py
from typing import Dict, Any
from .base import NotificationProvider
import sms_client


class TwilioProvider(NotificationProvider):
    """
    Strategy wrapper around sms_client.py.

    Expected payload keys:
    - 'number': recipient phone number (e.g. '+60123456789')
    - 'message': text body for WhatsApp
    """

    def send(self, payload: Dict[str, Any]) -> bool:
        number = payload.get("number")
        message = payload.get("message")

        if not number or not message:
            print("TwilioProvider: missing 'number' or 'message' in payload")
            return False

        try:
            # Delegate to existing implementation
            sms_client.main(number, message)
            return True
        except Exception as e:
            print("TwilioProvider error:", e)
            return False
