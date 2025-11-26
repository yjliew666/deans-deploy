from django.db import models

'''
    This model is deprecated
'''

class SocialMediaAccount(models.Model):
    social_media = models.CharField(default=None, max_length=255)
    social_account = models.CharField(default=None, max_length=255)
    def __str__(self):
        return self.social_account

    class Meta:
        pass