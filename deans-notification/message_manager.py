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



app = Flask(__name__)

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


if __name__ == '__main__':
    import os
    if('IN_DOCKER' in os.environ and os.environ['IN_DOCKER']=='1'):
        DEBUG = not ('PRODUCTION' in os.environ and os.environ['PRODUCTION']=='1')
        app.run(host='0.0.0.0', port=8000, debug=DEBUG)
    else:
         app.run(host='127.0.0.1', port=8000, debug=True)