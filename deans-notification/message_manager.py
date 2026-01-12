'''
Written by Michelle Lim Shi Hui & Nicholas Phang
Dean's Crisis Management System - Notification Subsystem
For CZ3003 Software System Analysis & Design

Message Manager -
API Server that receives JSON requests through API endpoints & processes them
'''
from flask import Flask, request, Response
from datetime import datetime
import json
import traceback

from providers.registry import PROVIDERS


import logging

from configparser import ConfigParser
import smtplib
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException
import tweepy
import facebook

app = Flask(__name__)
report_count = 1
logger = logging.getLogger(__name__)

@app.route('/')
def hello_world():
    return "hello world!"

'''
JSON format:
{"message":{
    "twitterShare": String,
    "facebookShare":{
        "shelterURL" : String, 
        "deansURL": String,
        "text": String,
        "recent_resolved_crisis":[],
        "new_crisis":[],
        "active_crisis":[]
    }
}
}
'''

@app.route('/socialmessages/', methods=['POST'])
def post_social_message():
    """
    JSON format:
    {
      "message": {
        "twitterShare": "string",
        "facebookShare": {
          "shelterURL": "string",
          "deansURL": "string",
          "text": "string",
          "recent_resolved_crisis": [],
          "new_crisis": [],
          "active_crisis": []
        }
      }
    }
    """
    try:
        data = request.get_json(force=True)
        print("Incoming /socialmessages payload:", data)

        message = data.get("message", {})
        provider = PROVIDERS["social"]
        ok = provider.send(message)

        if not ok:
            raise RuntimeError("SocialProvider failed to post to one or more channels")

        json_response = {"result": "Success!", "posted": message}
        return Response(json.dumps(json_response), status=201, mimetype="application/json")

    except Exception as e:
        traceback.print_exc()
        error_response = {"result": "Failure", "error": str(e)}
        return Response(json.dumps(error_response), status=500, mimetype="application/json")


@app.route('/dispatchnotices/', methods=['POST'])
def post_dispatch_notice():
    """
    JSON format:
    {
      "number": "+60123456789",
      "message": "Some crisis notice text"
    }
    """
    try:
        data = request.get_json(force=True)
        number = data.get("number")
        message_text = data.get("message")

        print("Incoming /dispatchnotices payload:", data)

        provider = PROVIDERS["whatsapp"]
        ok = provider.send({
            "number": number,
            "message": message_text,
        })

        if not ok:
            raise RuntimeError("TwilioProvider failed to send WhatsApp notice")

        json_response = {"result": "Success!", "sent_to": number, "posted": message_text}
        return Response(json.dumps(json_response), status=201, mimetype="application/json")

    except Exception as e:
        traceback.print_exc()
        error_response = {"result": "Failure", "error": str(e)}
        return Response(json.dumps(error_response), status=500, mimetype="application/json")

@app.route('/reports/', methods=['POST'])
def generate_report():
    """
    JSON format (actual fields come from core API):
    {
      "email": "recipient@example.com",
      ... crisis data ...
    }
    """
    try:
        print("Called /reports")
        data = request.get_json(force=True)
        print("Received data:", data)

        emailadd = data.get("email")
        if not emailadd:
            raise ValueError("Missing 'email' in request body")

        subject = "Crisis Summary Report for " + datetime.now().strftime("%I:%M%p on %B %d, %Y")

        # In our provider design, we pass 'data' as the crisis payload used by email_client.prettyPrintReport
        payload = {
            "email": emailadd,
            "subject": subject,
            "data": data,  # full crisis data dict
        }

        provider = PROVIDERS["email_report"]
        ok = provider.send(payload)

        if not ok:
            raise RuntimeError("ReportEmailProvider failed to send email report")

        json_response = {"result": "Success!", "sent_to": emailadd}
        return Response(json.dumps(json_response), status=201, mimetype="application/json")

    except Exception as e:
        traceback.print_exc()
        error_response = {"result": "Failure", "error": str(e)}
        return Response(json.dumps(error_response), status=500, mimetype="application/json")


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and orchestration.
    Validates connectivity to external services.
    """
    checks = {}
    overall_status = "healthy"
    status_code = 200
    
    # Load config once
    config = ConfigParser()
    try:
        config.read('config.ini')
    except Exception as e:
        logger.error(f"Failed to read config.ini: {e}")
        return Response(
            json.dumps({
                "status": "unhealthy",
                "error": "Configuration file missing",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }),
            status=503,
            mimetype='application/json'
        )
    
    # Check 1: Twilio (WhatsApp)
    try:
        account_sid = config.get('twilio', 'account_sid')
        token = config.get('twilio', 'token')
        client = TwilioClient(account_sid, token)
        
        # Validate credentials by fetching account info (lightweight)
        account = client.api.accounts(account_sid).fetch()
        checks["twilio"] = {
            "status": "up",
            "account_status": account.status
        }
        logger.debug("Twilio health check passed")
    except TwilioRestException as e:
        checks["twilio"] = {
            "status": "down",
            "error": f"Twilio API error: {e.msg}",
            "code": e.code
        }
        overall_status = "degraded"
        logger.error(f"Twilio health check failed: {e}")
    except Exception as e:
        checks["twilio"] = {
            "status": "down",
            "error": str(e)
        }
        overall_status = "degraded"  # Config issue, not critical
        logger.warning(f"Twilio config error: {e}")
    
    # Check 2: Facebook
    try:
        page_id = config.get('facebook', 'page_id')
        token = config.get('facebook', 'user_token')
        
        if not token or len(token) < 10:
            raise ValueError("Invalid Facebook token")
        
        # Lightweight check: validate token without posting
        graph = facebook.GraphAPI(access_token=token)
        # Get token info (doesn't post anything)
        graph.get_object('me')
        
        checks["facebook"] = {
            "status": "up",
            "token_valid": True
        }
        logger.debug("Facebook health check passed")
    except facebook.GraphAPIError as e:
        checks["facebook"] = {
            "status": "down",
            "error": str(e),
            "code": getattr(e, 'code', 'unknown')
        }
        overall_status = "degraded"  # Social media is non-critical
        logger.warning(f"Facebook health check failed: {e}")
    except Exception as e:
        checks["facebook"] = {
            "status": "down",
            "error": str(e)
        }
        overall_status = "degraded"
        logger.warning(f"Facebook config error: {e}")
    
    # Check 3: Twitter
    try:
        ckey = config.get('twitter', 'ckey')
        csecret = config.get('twitter', 'csecret')
        atoken = config.get('twitter', 'atoken')
        asecret = config.get('twitter', 'asecret')
        
        auth = tweepy.OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        api = tweepy.API(auth)
        
        # Lightweight check: verify credentials
        api.verify_credentials()
        
        checks["twitter"] = {
            "status": "up",
            "authenticated": True
        }
        logger.debug("Twitter health check passed")
    # except tweepy.TweepyException as e:
    #     checks["twitter"] = {
    #         "status": "down",
    #         "error": str(e)
    #     }
    #     overall_status = "degraded"
    #     logger.warning(f"Twitter health check failed: {e}")
    except Exception as e:
        checks["twitter"] = {
            "status": "down",
            "error": str(e)
        }
        overall_status = "degraded"
        logger.warning(f"Twitter health check failed: {e}")
    
    # Check 4: SMTP (Email)
    try:
        user = config.get('gmail', 'user')
        password = config.get('gmail', 'password')
        
        # Test SMTP connection (don't send email)
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
        server.starttls()
        server.login(user, password)
        server.quit()
        
        checks["smtp"] = {
            "status": "up",
            "server": "smtp.gmail.com"
        }
        logger.debug("SMTP health check passed")
    except smtplib.SMTPAuthenticationError as e:
        checks["smtp"] = {
            "status": "down",
            "error": "Authentication failed"
        }
        overall_status = "degraded"
        logger.warning(f"SMTP health check failed: {e}")
    except Exception as e:
        checks["smtp"] = {
            "status": "down",
            "error": str(e)
        }
        overall_status = "degraded"
        logger.warning(f"SMTP error: {e}")
    
        # Determine final status code
    if overall_status == "unhealthy":
        status_code = 503
    elif overall_status == "degraded":
        status_code = 200  # Still return 200 for degraded - service is running

    response_data = {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": checks,
        "service": "notification",
        "version": "1.0.0"
    }
    
    return Response(
        json.dumps(response_data),
        status=status_code,
        mimetype='application/json'
    )


@app.route('/ready', methods=['GET'])
def readiness_check():
    """
    Lightweight readiness check - just verify Flask is responding.
    """
    return Response(
        json.dumps({
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }),
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    import os
    if('IN_DOCKER' in os.environ and os.environ['IN_DOCKER']=='1'):
        DEBUG = not ('PRODUCTION' in os.environ and os.environ['PRODUCTION']=='1')
        app.run(host='0.0.0.0', port=4455, debug=DEBUG)
    else:
         app.run(host='127.0.0.1', port=4455, debug=True)