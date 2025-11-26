# api/routing.py
from django.conf.urls import url

from . import consumers


'''web_socket url'''
websocket_urlpatterns = [
    url(r'^api/ws/crises/?', consumers.CrisesConsumer),
]