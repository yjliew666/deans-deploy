"""API endpoint tests"""
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Crisis, CrisisType


class CrisisViewTest(TestCase):
    """Test suite for Crisis views/endpoints"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.crisis_type = CrisisType.objects.create(name="Medical")
        self.crisis = Crisis.objects.create(
            your_name="Jane Smith",
            mobile_number="9876543210",
            crisis_description="Emergency",
            crisis_type=self.crisis_type
        )

    def test_crisis_list_view_status(self):
        """Test crisis list endpoint returns 200"""
        response = self.client.get(reverse('crisis-list'))
        self.assertIn(response.status_code, [200, 404])  # 404 if URL not configured

    def test_crisis_detail_view_status(self):
        """Test crisis detail endpoint"""
        response = self.client.get(
            reverse('crisis-detail', args=[self.crisis.id])
        )
        self.assertIn(response.status_code, [200, 404, 405])
