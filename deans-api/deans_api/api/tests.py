from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import (
    Crisis,
    CrisisAssistance,
    CrisisType,
    SiteSettings,
    EmergencyAgencies
)


class CrisisModelTest(TestCase):
    """Test suite for Crisis model"""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for Crisis model tests"""
        Crisis.objects.create(
            your_name="yuance",
            mobile_number="83496888",
            crisis_description="HELP!"
        )

    def test_crisis_model_your_name_max_length(self):
        """Test that your_name field has max_length of 255"""
        crisis = Crisis.objects.get(your_name="yuance")
        max_length = crisis._meta.get_field('your_name').max_length
        self.assertEqual(max_length, 255)

    def test_crisis_model_string_representation(self):
        """Test string representation of Crisis model"""
        crisis = Crisis.objects.get(your_name="yuance")
        self.assertEqual(str(crisis), crisis.your_name)

    def test_crisis_mobile_number_field(self):
        """Test mobile_number field is saved correctly"""
        crisis = Crisis.objects.get(your_name="yuance")
        self.assertEqual(crisis.mobile_number, "83496888")

    def test_crisis_description_field(self):
        """Test crisis_description field is saved correctly"""
        crisis = Crisis.objects.get(your_name="yuance")
        self.assertEqual(crisis.crisis_description, "HELP!")


class CrisisAPITest(TestCase):
    """Test suite for Crisis API endpoints"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.crisis_data = {
            "your_name": "test_user",
            "mobile_number": "1234567890",
            "crisis_description": "Test crisis"
        }

    def test_crisis_creation_via_api(self):
        """Test creating a crisis via API"""
        # This is a placeholder - adjust URL and method based on your API
        response = self.client.post(
            reverse('crisis-list'),
            self.crisis_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_crisis_list_endpoint(self):
        """Test retrieving list of crises"""
        Crisis.objects.create(**self.crisis_data)
        response = self.client.get(reverse('crisis-list'))
        self.assertEqual(response.status_code, 200)
