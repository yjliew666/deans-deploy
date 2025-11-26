'''
Written by Michelle Lim Shi Hui & Nicholas Phang
Dean's Crisis Management System - Notification Subsystem
For CZ3003 Software System Analysis & Design

Facebook API -
Takes in Facebook credentials & message, formats the message & posts it
Leverages on Facebook's Graph API
'''

import facebook

#Get API keys
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
page_id = config.get('facebook', 'page_id')

token = config.get('facebook', 'user_token')

def main(data):

    graph = facebook.GraphAPI(access_token = token)
    print("Connection to Facebook success")
    formatted_text = format(data)
    print("Facebook Received: " + formatted_text)
    graph.put_object(parent_object='me',
                     connection_name='feed',
                     message=formatted_text,
                     link=data['deansURL'])
    print("Post to Facebook success")

def format(data):
    formatted_text = data['text']
    return formatted_text