'''
Written by Michelle Lim Shi Hui & Nicholas Phang
Dean's Crisis Management System - Notification Subsystem
For CZ3003 Software System Analysis & Design

Message Manager -
API Server that receives JSON requests through API endpoints & processes them
'''
from flask import Flask, request, Response
from datetime import datetime
import report_generation
import facebook_client
import sms_client
import twitter_client
import json
import traceback
import email_client
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

# JSON format: {"message" : string}
@app.route('/socialmessages/', methods=['POST'])
def post_social_message():
    try :
        data = request.get_json()
        print(data)
        message = data['message']
        print('Connecting to Twitter...')
        twitter_client.main(message['twitterShare'])
        print('Connecting to Facebook...')
        facebook_client.main(message['facebookShare'])
        json_response = {"result" : "Success!", "posted" : message}

        return Response(json.dumps(json_response), status=201, mimetype='application/json')

    except Exception as e:
        traceback.print_tb(e.__traceback__)

# JSON format: {"number" : string, "message" : string}
@app.route('/dispatchnotices/', methods=['POST'])
def post_dispatch_notice():
    data = request.get_json()
    number = data['number']
    message = data['message']
    print('Connecting to Twilio...')
    sms_client.main(number, message)
    json_response = {"result": "Success!", "sent_to": number, "posted": message}
    return Response(json.dumps(json_response), status=201, mimetype='application/json')

'''
JSON format:
{"email" : email address, 
"cases" : 
[{
        "crisis_time" : datetime, 
        "resolved_by" : datetime,
        "location" : location,
        "crisis_type" : string,
        "crisis_description" : string,
        "crisis_assistance": string
},
]}
'''
@app.route('/reports/', methods=['POST'])
def generate_report():
    print("Called")
    # global report_count
    data = request.get_json()
    time_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # json_file = "json_summary/report_" + time_stamp + ".json"
    # with open(json_file, 'w+') as f:
    #     json.dump(data, f)
    print("received data", data)
    # report_generation.json_to_pdf(report_count)
    print('Generating Report...')
    # report = "reports/report"+str(report_count)+'.pdf'
    # report_count += 1

    print('Connecting to Gmail...')
    emailadd = data['email']
    subject = "Crisis Summary Report for " + datetime.now().strftime("%I:%M%p on %B %d, %Y")
    # email_client.main(emailadd, subject, report)
    email_client.main(emailadd, subject, data)
    json_response = {"result": "Success!", "sent_to": emailadd}
    return Response(json.dumps(json_response), status=201, mimetype='application/json')

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
        app.run(host='0.0.0.0', port=8000, debug=DEBUG)
    else:
         app.run(host='127.0.0.1', port=8000, debug=True)