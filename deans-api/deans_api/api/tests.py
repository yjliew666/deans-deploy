from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    Crisis,
    CrisisAssistance,
    CrisisType,
    SiteSettings,
    EmergencyAgencies
    )
# Create your tests here.

class YourTestClass(TestCase):
	@classmethod
	def setUpTestData(self):
		Crisis.objects.create(your_name="yuance",
			mobile_number="83496888",
			crisis_description="HELP!")
	def test_model_crsis_1(self):
		yuance=Crisis.objects.get(your_name="yuance")
		max_length = yuance._meta.get_field('your_name').max_length
		self.assertEquals(max_length, 255)
