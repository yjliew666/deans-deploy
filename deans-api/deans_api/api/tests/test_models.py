"""Model tests for Crisis, CrisisAssistance, etc."""
from django.test import TestCase
from ..models import Crisis, CrisisType, EmergencyAgencies


class CrisisModelTest(TestCase):
    """Test suite for Crisis model"""

    @classmethod
    def setUpTestData(cls):
        """Set up test data"""
        cls.crisis_type = CrisisType.objects.create(name="Medical")
        cls.crisis = Crisis.objects.create(
            your_name="John Doe",
            mobile_number="1234567890",
            crisis_description="Medical emergency",
            crisis_type=cls.crisis_type
        )

    def test_crisis_creation(self):
        """Test crisis can be created"""
        self.assertTrue(Crisis.objects.exists())

    def test_crisis_your_name_field(self):
        """Test your_name field properties"""
        crisis = Crisis.objects.get(your_name="John Doe")
        self.assertEqual(crisis.your_name, "John Doe")
        max_length = crisis._meta.get_field('your_name').max_length
        self.assertEqual(max_length, 255)

    def test_crisis_mobile_number_field(self):
        """Test mobile_number field"""
        crisis = Crisis.objects.get(your_name="John Doe")
        self.assertEqual(crisis.mobile_number, "1234567890")
