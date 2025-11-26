from django.db import models
'''
    EmergencyAgencies model consists the agency id and the agency name, phone number of each emergency agency object.
'''
class EmergencyAgencies(models.Model):
    agency_id = models.AutoField(primary_key=True)
    agency = models.CharField(default=None, max_length=255)
    phone_number = models.CharField(default=None, max_length=255)
    def __str__(self):
        return self.agency

    class Meta:
        pass