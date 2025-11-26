'''
Written by Michelle Lim Shi Hui & Nicholas Phang
Dean's Crisis Management System - Notification Subsystem
For CZ3003 Software System Analysis & Design

Twitter API -
Takes in twitter credentials & message, formats the message & posts it
Leverages on Tweepy package to connect to Twitter API endpoint
'''

import tweepy

#Get API keys
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
ckey = config.get('twitter', 'ckey')
csecret = config.get('twitter', 'csecret')
atoken = config.get('twitter', 'atoken')
asecret = config.get('twitter', 'asecret')

## TODO: IMPLEMENT ERROR HANDLING IF EXCESS 140 CHAR

def main(data):
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    print('Twitter Authentication Complete')
    api = tweepy.API(auth)
    post(api, data)

def post(api, data):
    api.update_status(data)
    print(data)
    print("Twitter Post Successful")

