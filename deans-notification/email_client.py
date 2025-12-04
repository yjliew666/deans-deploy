'''
Written by Michelle Lim Shi Hui & Nicholas Phang
Dean's Crisis Management System - Notification Subsystem
For CZ3003 Software System Analysis & Design

Email Manager -
Takes in email address list & message, formats it, and sends out the email
Leverages on smtplib
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

import pprint

#Get API keys
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
user = config.get('gmail', 'user')
password = config.get('gmail', 'password')

def prettyPrintReport(data):
    message = ""
    message += "-------------------------------------------------------------------------------------------\n"
    message += "                          New Crises Reported in Past 30 Minutes     \n"
    message += "-------------------------------------------------------------------------------------------\n\n"

    for crisis in data['new_crisis']:
        message += "Report Time: " + crisis['crisis_time'] + "\n"
        message += "Location: " + crisis['location'] + "\n"
        message += "Location2: " + crisis['location2'] + "\n"
        message += "Crisis Type: " + crisis['type'] + "\n"
        message += "Assistance Requested: " + crisis['crisis_assistance'] + "\n"
        message += "Description: " + crisis['crisis_description'] + "\n"
        message += "\n"
    message += "-------------------------------------------------------------------------------------------\n"
    message += "                          Crises Resolved in Past 30 Minutes       \n"
    message += "-------------------------------------------------------------------------------------------\n\n"
    for crisis in data['recent_resolved_crisis']:
        message += "Report Time: " + crisis['crisis_time'] + "\n"
        message += "Location: " + crisis['location'] + "\n"
        message += "Location2: " + crisis['location2'] + "\n"
        message += "Crisis Type: " + crisis['type'] + "\n"
        message += "Assistance Requested: " + crisis['crisis_assistance'] + "\n"
        message += "Description: " + crisis['crisis_description'] + "\n"
        message += "\n"

    message += "-------------------------------------------------------------------------------------------\n"
    message += "                          Current Unresolved Crisis           \n"
    message += "-------------------------------------------------------------------------------------------\n\n"
    for crisis in data['active_crisis']:
        message += "Report Time: " + crisis['crisis_time'] + "\n"
        message += "Location: " + crisis['location'] + "\n"
        message += "Location2: " + crisis['location2'] + "\n"
        message += "Crisis Type: " + crisis['type'] + "\n"
        message += "Assistance Requested: " + crisis['crisis_assistance'] + "\n"
        message += "Description: " + crisis['crisis_description'] + "\n"
        message += "\n"

    return message


def main(emailadd, subject, data):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = emailadd
    msg['Subject'] = subject
    body = """ 
Dear Prime Minister,
    
Here is the report as of %s. 

%s
    
Best regards,
Dean's Crisis Management System
    
This is an auto-generated message. Please do not reply.
    """ % (datetime.now().strftime("%I:%M %p on %B %d, %Y"), prettyPrintReport(data))
    msg.attach(MIMEText(body, 'plain'))

    # filename = report
    # attachment = open(filename, 'rb')

    # part = MIMEBase('application', 'octet-stream')
    # part.set_payload(attachment.read())
    # encoders.encode_base64(part)
    # part.add_header('Content-Disposition', "attachment; filename= "+filename[filename.index("/")+1:])

    # msg.attach(part)

    text = msg.as_string()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        print('Connection to Gmail Success!')
        server.sendmail(user, emailadd, text)
        server.quit()
        print('Email sent!')
    except:
        #TODO: Exception Handling
        print('Something went wrong...')

