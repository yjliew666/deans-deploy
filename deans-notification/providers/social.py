# providers/social.py
from typing import Dict, Any
from .base import NotificationProvider
import facebook_client
import twitter_client


class SocialProvider(NotificationProvider):
    """
    Composite provider that posts to Twitter and Facebook.
    Payload is the 'message' dict from /socialmessages:
    {
      "twitterShare": "text for tweet",
      "facebookShare": {...}
    }
    """

    def send(self, payload: Dict[str, Any]) -> bool:
        twitter_text = payload.get("twitterShare")
        facebook_payload = payload.get("facebookShare")

        if not twitter_text or not facebook_payload:
            print("SocialProvider: missing twitterShare or facebookShare")
            return False

        ok_twitter = ok_facebook = True

        try:
            print("Connecting to Twitter...")
            twitter_client.main(twitter_text)
        except Exception as e:
            print("Twitter error:", e)
            ok_twitter = False

        try:
            print("Connecting to Facebook...")
            facebook_client.main(facebook_payload)
        except Exception as e:
            print("Facebook error:", e)
            ok_facebook = False

        return ok_twitter and ok_facebook
