# Dean's Crisis Management System - Notification Subsystem
> This subsystem takes a message from the API subsystem, parses it, and redirects it to the relevant destination: Email, WhatsApp, or Facebook & Twitter. 


## How to Start

Windows:

1. Clone the repository
```sh
git clone git://github.com/Deans-CMS/deans-notification.git
```

2. Install dependencies
```sh
pip install-r requirements.txt
```

3. Start server (the API server will start on 	**localhost:8000**)
```sh
python message_manager.py
```

4. Set up Twilio

As WhatsApp for Twilio is still in Sandbox mode, please connect your WhatsApp number to Sandbox to receive messages through Twilio.
> Send a WhatsApp message to **+1 415 523 8886** with the code ```join coquelicot-labradoodle```.

## API Endpoints

1. Facebook & Twitter ```/socialmessages/```

Takes a JSON file of format ```{"message" : string}``` and posts the message to Dean CMS' Facebook & Twitter pages, returning a HTTP Response of status code ```201``` if successfully posted.

**NOTE: Facebook App is still in development mode, only developers can see the posts posted. Still in process of App Review.**

>Example:
```sh
POST /socialmessages/ HTTP/1.1
Host: localhost
Content-Type: application/json
cache-control: no-cache
Postman-Token: 2f604143-450a-45e9-bf85-a5442d3173b0
{"message" : "hello world!"}
```

2. WhatsApp ```/dispatchnotices/```

Takes a JSON file of format ```{"number" : phone number (with country code), "message" : string}``` and sends a WhatsApp message to the specified number pages, returning a HTTP Response of status code ```201``` if successfully sent.

**NOTE: The number MUST be connected to Twilio's Sandbox in order to successfully receive messages, otherwise it will fail.**

>Example:
```sh
POST /dispatchnotices/ HTTP/1.1
Host: localhost
Content-Type: application/json
cache-control: no-cache
Postman-Token: fde35f4e-0cd6-4178-8b13-65c274d0bb9b
{"number":"+6586830963","message":"URGENT: Fire @ 38 Nanyang Cres, Singapore 636866. Block 24 #06-120."}
```

3. Email Reports ```/reports/```

Accepts a JSON file of ```{"email" : email address, "cases" : list of json records}```, uses Jasper Reports to generate a pdf version of the JSON data received, and emails it as an attachment to the specified email address. 

HTTP Response of status code ```201``` returned if successfully sent.

>Example:
```sh
POST /reports/ HTTP/1.1
Host: localhost
Content-Type: application/json
cache-control: no-cache
Postman-Token: eb29d4bb-3500-4155-b17b-e478f203dab4
{
  "email":"michellelimsh@gmail.com",
  "cases":[
    {"crisis_time" : "16:15:30",
      "resolved_by" : "18:32:15",
      "crisis_type": "Fire Breakout",
      "crisis_description": "Fire!!!",
      "crisis_assistance": "Fire Fighting",
      "crisis_location": "24 Nanyang Crescent Block 24 #06-23"
},
    {"crisis_time" : "17:53:25",
      "resolved_by" : "18:37:23",
      "crisis_type": "Casualty",
      "crisis_description": "Heart Attack",
      "crisis_assistance": "Emergency Ambulance",
      "crisis_location": "112 Boon Lay Avenue 6 Block 112 #06-23"
},
{
  ...
}, ...
]
}
```

## Accounts:

Email account: deanscms@gmail.com

Facebook Page: https://www.facebook.com/deans.cms/ 

Twitter Account: https://twitter.com/dean_cms
