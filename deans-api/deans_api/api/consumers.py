import json
import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# Initialize Logger
logger = logging.getLogger(__name__)


class CrisesConsumer(WebsocketConsumer):
  """
  Handles WebSocket connections for real-time Crisis updates.
  Uses standard WebsocketConsumer to maintain the original 'receive' method signature.
  """
  GROUP_NAME = "crises"

  def connect(self):
    """
    Perform things on connection start.
    """
    try:
      # Join the group
      async_to_sync(self.channel_layer.group_add)(
          self.GROUP_NAME,
          self.channel_name
      )
      self.accept()
      logger.info(f"WebSocket Connected: {self.channel_name}")
    except Exception as e:
      logger.error(f"Error connecting WebSocket: {e}")
      self.close()

  def disconnect(self, close_code):
    """
    Perform things on connection close.
    Note: Standard Channels signature uses 'close_code', not 'message'.
    """
    try:
      async_to_sync(self.channel_layer.group_discard)(
          self.GROUP_NAME,
          self.channel_name
      )
      logger.info(
        f"WebSocket Disconnected: {self.channel_name} (Code: {close_code})")
    except Exception as e:
      logger.error(f"Error disconnecting WebSocket: {e}")

  def receive(self, text_data):
    """
    Called when a message is received from the client.
    Kept strict to original method name.
    """
    logger.debug(f"Received message from client: {text_data}")
    pass

  def crises_update(self, event):
    """
    Called when a message is received from redis (the Channel Layer).
    """
    try:
      payload = event.get("payload", {})
      self.send(text_data=json.dumps(payload))
      logger.debug(f"Broadcasted crisis update to {self.channel_name}")
    except Exception as e:
      logger.error(f"Failed to broadcast crisis update: {e}")