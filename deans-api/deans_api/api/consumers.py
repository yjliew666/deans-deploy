# from .models import Crisis
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Crisis
from .serializer import CrisisSerializer
from rest_framework.response import Response

class CrisesConsumer(WebsocketConsumer):

    def connect(self):
        """
        Perform things on connection start
        """
        # Join group
        async_to_sync(self.channel_layer.group_add)(
            "crises",
            self.channel_name
        )
        
        self.accept()

    def receive(self, text_data):
        """
        Called when a message is received
        """
        pass
    
    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            "crises",
            self.channel_name
        )

    def crises_update(self, event):
        """
        Called when a message is received from redis
        """
        payload = event["payload"]
        self.send(payload)