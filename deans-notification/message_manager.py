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

app = Flask(__name__)
report_count = 1

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

if __name__ == '__main__':
    import os
    if('IN_DOCKER' in os.environ and os.environ['IN_DOCKER']=='1'):
        DEBUG = not ('PRODUCTION' in os.environ and os.environ['PRODUCTION']=='1')
        app.run(host='0.0.0.0', port=8000, debug=DEBUG)
    else:
         app.run(host='127.0.0.1', port=8000, debug=True)