# providers/report_email.py
from typing import Dict, Any
from .base import NotificationProvider
import email_client


class ReportEmailProvider(NotificationProvider):
    """
    Strategy wrapper around email_client.py

    Expected payload keys:
    - 'email': recipient email address (string)
    - 'subject': subject line (string)
    - 'data': dict with crisis data:
        {
          "new_crisis": [...],
          "recent_resolved_crisis": [...],
          "active_crisis": [...]
        }
    """

    def send(self, payload: Dict[str, Any]) -> bool:
        email = payload.get("email")
        subject = payload.get("subject")
        data = payload.get("data")

        if not email or not subject or data is None:
            print("ReportEmailProvider: missing 'email', 'subject' or 'data'")
            return False

        try:
            email_client.main(email, subject, data)
            return True
        except Exception as e:
            print("ReportEmailProvider error:", e)
            return False
