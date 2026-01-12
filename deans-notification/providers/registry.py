# providers/registry.py

from typing import Dict
from .base import NotificationProvider
from .facebook import FacebookProvider
from .twitter import TwitterProvider
from .social import SocialProvider
from .twilio import TwilioProvider
from .report_email import ReportEmailProvider
from .report_pdf import ReportPDFProvider
from .telegram import TelegramProvider

facebook_provider = FacebookProvider()
twitter_provider = TwitterProvider()
social_provider = SocialProvider()
twilio_provider = TwilioProvider()
report_email_provider = ReportEmailProvider()
report_pdf_provider = ReportPDFProvider()

PROVIDERS: Dict[str, NotificationProvider] = {
    "facebook": facebook_provider,
    "twitter": twitter_provider,
    "social": social_provider,
    "whatsapp": twilio_provider,
    "email_report": report_email_provider,
    "pdf_report": report_pdf_provider,
    "telegram": TelegramProvider(),  # new example channel
}
