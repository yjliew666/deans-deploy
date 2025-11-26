from django.contrib.auth.models import User 
from django.db import models
from .CrisisType import CrisisType
from .Operator import Operator
from .CrisisAssistance import CrisisAssistance
from django.db.models import signals
import requests
import datetime
import channels.layers
from asgiref.sync import async_to_sync
from rest_framework.response import Response # this is bad!
import json
import logging
logger = logging.getLogger("django")

STATUS_CHOICES = (
    ('PD', 'Pending'),
    ('DP', 'Dispatched'),
    ('RS', 'Resolved'),
)
'''
    This is the most important model of the whole CMS System. The Crisis Model consists of all the information that a crisis needs.
    Details:
        reporter's name,  String
        reporter's mobile_number, String
        crisis_id, String
        crisis_type, Many to many field linked to CrisisType Model
        crisis_description, longer String, Text Field
        crisis_assistance, Many to many field linked to CrisisAssistance Model
        crisis_assistance_description, longer string, Text Field
        crisis_time, a date time field
        crisis_location1&2, longer String, Text field
        updated_at, a date time field records last object modification
        owner, a Many to many field linked to User Model
        visible, a boolean field recording the visibility of a crisis in the front end
        dispatch_trigger, a boolean field recording the signal of a dispatch action
        crisis status, a tuple recording the crisis status
'''
class Crisis(models.Model):
    your_name = models.CharField(default=None,max_length=255)
    mobile_number = models.CharField(default=None,max_length=255)
    crisis_id = models.AutoField(primary_key=True)
    crisis_type = models.ManyToManyField(CrisisType)
    crisis_description = models.TextField(default="")
    crisis_assistance = models.ManyToManyField(CrisisAssistance)
    crisis_assistance_description = models.TextField(default="")
    crisis_time = models.DateTimeField(auto_now_add=True)
    crisis_location1 = models.TextField()
    crisis_location2 = models.TextField(default="")
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ManyToManyField(User)
    visible = models.BooleanField(default=True)
    phone_number_to_notify = models.CharField(default="",max_length=255)
    dispatch_trigger = models.BooleanField(default=False)

    crisis_status = models.CharField(choices=STATUS_CHOICES, default='PD',  max_length=254)

    def __str__(self):
        return str(self.crisis_id)

    class Meta:
        ordering = ['-crisis_id']

'''
    social media announcement generator
'''

def construct_social_media_data(this_crisis):
    payload = {}

    # shelter location url, immediate Crisis, recent_resolved_crisis, Dispatched Crisis,

    created_time = datetime.datetime.now() - datetime.timedelta(minutes=30)  # crisis created since 30 mins ago
    recent_resolved_crisis = Crisis.objects.filter(updated_at__gte=created_time, crisis_status="RS")
    active_crisis = Crisis.objects.exclude(crisis_status="RS")

    payload['postTime'] = created_time.strftime('%Y-%m-%d %H:%M')
    payload['deansURL'] = "https://deans.csming.com/"
    payload['shelterURL'] = "https://deans.csming.com/"
    payload['recent_resolved_crisis'] = []
    payload['active_crisis'] = []
    payload['new_crisis'] = []
    print("payload", payload)

    payload['new_crisis'].append({
        "crisis_time": this_crisis.crisis_time.strftime("%Y-%m-%d %H:%M:%S"),
        "resolved_by": this_crisis.updated_at.strftime("%Y-%m-%d %H:%M:%S") if this_crisis.crisis_status == "RS" else "None",
        "location": this_crisis.crisis_location1,
        "location2": this_crisis.crisis_location2,
        "type": ", ".join([j.name for j in this_crisis.crisis_type.all()]),
        "status": this_crisis.crisis_status,
        "crisis_description": this_crisis.crisis_description,
        "crisis_assistance": ", ".join([j.name for j in this_crisis.crisis_assistance.all()]),
        "assistance_description": this_crisis.crisis_assistance_description
    }
    )

    reported_time = str(this_crisis.crisis_time)
    name = this_crisis.your_name
    mobile_number = this_crisis.mobile_number
    location1 = this_crisis.crisis_location1
    location2 = this_crisis.crisis_location2
    # create crisis type
    crisis_type_queryset = this_crisis.crisis_type.all()
    crisis_type = []
    for _ in crisis_type_queryset:
        crisis_type.append(str(_))
    crisis_type = ", ".join(crisis_type)
    # create assistance type
    assistance_type_queryset = this_crisis.crisis_assistance.all()
    assistance_type = []
    for _ in assistance_type_queryset:
        assistance_type.append(str(_))
    assistance_type = ", ".join(assistance_type)
    # handle the rest
    crisis_description = this_crisis.crisis_description
    assistance_description = this_crisis.crisis_assistance_description

    message = "\nWe have received the following crisis report, need your immediate attention:\n\n"
    message += "Reported Time: " + reported_time + "\n"
    message += "Location: " + location1 + "\n"
    message += "Location2: " + location2 + "\n"
    message += "Crisis Type: " + crisis_type + "\n"
    message += "Crisis Description: " + crisis_description + "\n"
    message += "Requested Assistance: " + assistance_type + "\n"
    message += "Assistance Description: " + assistance_description + "\n"

    payload['text'] = message

    for i in recent_resolved_crisis:
        payload['recent_resolved_crisis'].append(
            {
                "crisis_time": i.crisis_time.strftime("%Y-%m-%d %H:%M:%S"),
                "resolved_by": i.updated_at.strftime("%Y-%m-%d %H:%M:%S") if i.crisis_status == "RS" else "None",
                "location": i.crisis_location1,
                "location2": i.crisis_location2,
                "type": ", ".join([j.name for j in i.crisis_type.all()]),
                "status": i.crisis_status,
                "crisis_description": i.crisis_description,
                "crisis_assistance": ", ".join([j.name for j in i.crisis_assistance.all()]),
                "assistance_description": i.crisis_assistance_description
            }
        )
    for i in active_crisis:
        payload['active_crisis'].append(
            {
                "crisis_time": i.crisis_time.strftime("%Y-%m-%d %H:%M:%S"),
                "resolved_by": i.updated_at.strftime("%Y-%m-%d %H:%M:%S") if i.crisis_status == "RS" else "None",
                "location": i.crisis_location1,
                "location2": i.crisis_location2,
                "type": ", ".join([j.name for j in i.crisis_type.all()]),
                "status": i.crisis_status,
                "crisis_description": i.crisis_description,
                "crisis_assistance": ", ".join([j.name for j in i.crisis_assistance.all()]),
                "assistance_description": i.crisis_assistance_description
            }
        )
    return payload

'''
    notification subsystem - social media api caller trigger + dispatch action trigger
    when crisis model is saved, this trigger function is called.
    Social media api will be called to send announcement.
    dispatch function will only be called when there is a dispatch signal.
'''
def trigger(sender, instance, created, **kwargs):

    #Social media Trigger
    print("Doing Social Media Publishing...")
    url = "http://notification:8000/socialmessages/"
    this_crisis = Crisis.objects.get(pk=instance.pk)
    fb_payload = construct_social_media_data(this_crisis)
    tw_payload = "A Crisis is happening at time: {}!\n".format(fb_payload['postTime'])
    tw_payload += "For your safety. Shelter Information: " + fb_payload['shelterURL']
    tw_payload += "\nFor Crisis detail information: " + fb_payload['deansURL']

    print("payload: ", tw_payload)
    print("payload: ", fb_payload)
    print("Before sending")
    # Post to the notification system api, to send facebook and twitter announcement
    response = requests.post("http://notification:8000/socialmessages/",
                  json={"message": {"twitterShare":tw_payload, "facebookShare":fb_payload}},
                  headers={
                      'content-type': "application/json",
                  }
                  )
    print("Sent request")
    logger.info(response.status_code)
    logger.info('Have published to Facebook and Twitter.')

    # Dispatch
    if this_crisis.crisis_status == "DP":
        try:
            if sender.dispatch_trigger:
                phone_number_to_notify = json.loads(this_crisis.phone_number_to_notify)
                # start creating message
                reported_time = str(this_crisis.crisis_time)
                name = this_crisis.your_name
                mobile_number = this_crisis.mobile_number
                location1 = this_crisis.crisis_location1
                location2 = this_crisis.crisis_location2
                # create crisis type
                crisis_type_queryset = this_crisis.crisis_type.all()
                crisis_type = []
                for _ in crisis_type_queryset:
                    crisis_type.append(str(_))
                crisis_type = ", ".join(crisis_type)
                # create assistance type
                assistance_type_queryset = this_crisis.crisis_assistance.all()
                assistance_type = []
                for _ in assistance_type_queryset:
                    assistance_type.append(str(_))
                assistance_type = ", ".join(assistance_type)
                # handle the rest
                crisis_description = this_crisis.crisis_description
                assistance_description = this_crisis.crisis_assistance_description
                # construct message content
                message = "We have received the following crisis report, need your immediate attention:\n\n"
                message += "Reported Time: " + reported_time + "\n"
                message += "Reporter Name: " + name + "\n"
                message += "Mobile Number: " + mobile_number + "\n"
                message += "Location: " + location1 + "\n"
                message += "Location2: " + location2 + "\n"
                message += "Crisis Type: " + crisis_type + "\n"
                message += "Crisis Description: " + crisis_description + "\n"
                message += "Requested Assistance: " + assistance_type + "\n"
                message += "Assistance Description: " + assistance_description + "\n"
                message += "\nThank you for keeping our people safe!"

                print(message)

                for phone_number in phone_number_to_notify:
                    prefixed_phone_number = "+65" + str(phone_number)
                    requests.post("http://notification:8000/dispatchnotices/",
                                json={"number" : prefixed_phone_number, "message" : message},
                                headers={
                                    'content-type': "application/json",
                                    'cache-control': "no-cache"
                                }
                                )
        except Exception as e:
            print("It is ok.", e)

    '''
        Crisis Info, WebSocket cache service
    '''

    try:
        # send to redis
        queryset = Crisis.objects.all()
        from ..serializer import CrisisSerializer
        serializer = CrisisSerializer(queryset, many=True)
        response = Response(serializer.data) # response is an array of crises
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)("crises", {
            "type": "crises_update",
            "payload": json.dumps(list(response.data))
        })
    except Exception as e:
        print("It is not ok. Human lives at risk!", e)

signals.post_save.connect(receiver=trigger, sender=Crisis)

