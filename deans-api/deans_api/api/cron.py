import logging
import datetime
import requests
from typing import List, Dict, Any

from django.conf import settings
from django.utils import timezone
from django_cron import CronJobBase, Schedule
from .models import Crisis

# --- REENGINEERING CHANGE 1: Import Django Settings ---
from django.conf import settings
# ------------------------------------------------------

# Get the logger instance
logger = logging.getLogger(__name__)

# Configuration Constants
NOTIFICATION_URL = f"{settings.NOTIFICATION_SERVICE_URL}/reports/"
DEFAULT_REPORT_EMAIL = "deanscms@gmail.com"
REQUEST_TIMEOUT = 10  # seconds


def _serialize_crisis(crisis_obj: Crisis) -> Dict[str, Any]:
  """
  Helper function to convert a Crisis model instance into a dictionary.
  """
  # pre-calculate helper strings
  types_str = ", ".join([t.name for t in crisis_obj.crisis_type.all()])
  assistance_str = ", ".join(
      [a.name for a in crisis_obj.crisis_assistance.all()])

  resolved_time = "None"
  if crisis_obj.crisis_status == "RS":
    resolved_time = crisis_obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")

  return {
    "crisis_time": crisis_obj.crisis_time.strftime("%Y-%m-%d %H:%M:%S"),
    "resolved_by": resolved_time,
    "location": crisis_obj.crisis_location1,
    "location2": crisis_obj.crisis_location2,
    "type": types_str,
    "status": crisis_obj.crisis_status,
    "crisis_description": crisis_obj.crisis_description,
    "crisis_assistance": assistance_str,
    "assistance_description": crisis_obj.crisis_assistance_description
  }


def construct_report_data() -> Dict[str, Any]:
  """
  Fetches crisis data and constructs the JSON payload.
  """
  # Use Django's timezone aware now()
  cutoff_time = timezone.now() - datetime.timedelta(minutes=30)

  # Database queries
  new_crises = Crisis.objects.filter(crisis_time__gte=cutoff_time)
  recent_resolved_crises = Crisis.objects.filter(updated_at__gte=cutoff_time,
                                                 crisis_status="RS")
  active_crises = Crisis.objects.exclude(crisis_status="RS")

  logger.info(f"Report Generation: Found {new_crises.count()} new, "
              f"{recent_resolved_crises.count()} resolved, "
              f"{active_crises.count()} active crises.")

  payload = {
    'email': DEFAULT_REPORT_EMAIL,
    'new_crisis': [_serialize_crisis(c) for c in new_crises],
    'recent_resolved_crisis': [_serialize_crisis(c) for c in
                               recent_resolved_crises],
    'active_crisis': [_serialize_crisis(c) for c in active_crises],
  }

  return payload


class CronEmail(CronJobBase):
  RUN_EVERY_MINS = 1
  ALLOW_PARALLEL_RUNS = True

  schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
  code = 'api.CronEmail'

  def do(self):
    logger.info(f"Starting Cron Job: {self.code}")

    try:
      payload = construct_report_data()
      headers = {'Content-Type': "application/json"}

      logger.debug(f"Sending payload to {NOTIFICATION_URL}")

      response = requests.post(
          NOTIFICATION_URL,
          json=payload,
          headers=headers,
          timeout=REQUEST_TIMEOUT
      )

      # Check for HTTP errors (4xx or 5xx)
      response.raise_for_status()

      logger.info(
        "Successfully sent email report to President Office via Notification Service.")

    except requests.exceptions.RequestException as e:
      # Catches DNS failures, connection refused, timeouts, and 4xx/5xx responses
      logger.error(
        f"Failed to send report to Notification Service. Error: {str(e)}")
    except Exception as e:
      # Catches generic Python errors (e.g., database serialization issues)
      logger.exception(f"Unexpected error in {self.code}: {str(e)}")

# class CronSocialMedia(CronJobBase):
#     RUN_EVERY_MINS = 1
#     ALLOW_PARALLEL_RUNS = True
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'api.CronSocialMedia'
#     def do(self):
#         # --- REENGINEERING CHANGE 3: Decouple Social Media URL (conceptual) ---
#         # We apply the same logic here to decouple the second hardcoded URL
#         url = f"{settings.NOTIFICATION_SERVICE_URL}/socialmessages/"
#         # --------------------------------------------------------------------
#         payload = construct_report_data()
#         headers = {'Content-Type': "application/json"}
#         response = requests.request("POST", url, json=payload, headers=headers)
#         # logger.info(response.text)
#         logger.info('Sent message to social medias.')