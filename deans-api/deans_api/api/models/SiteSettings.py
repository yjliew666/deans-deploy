from django.db import models
from .CrisisType import CrisisType
from .CrisisAssistance import CrisisAssistance
#from .EmergencyAgencies import EmergencyAgencies
#from .SocialMediaAccount import SocialMediaAccount

'''
    SiteSetting model implements the design pattern of singleton.
    only one unique instance of the model will be created, loaded and deleted in the database.
'''
class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

'''
    facebook & twitter information together with the summary_report_email will be in the settings.
'''

class SiteSettings(SingletonModel):
    #setting_type = models.ForeignKey('CrisisType',default = None, on_delete=models.CASCADE)
    #setting_assistance = models.ForeignKey('CrisisAssistance',default = None, on_delete=models.CASCADE)
    # social_media_account = models.CharField(default=None, max_length=255)
    # social_media = models.CharField(default=None, max_length=255)
    #emergency_agencies = models.ForeignKey('EmergencyAgencies', default = None, on_delete=models.CASCADE)
    facebook_account = models.CharField(default=None, max_length=255)
    facebook_password = models.CharField(default=None, max_length=255)
    twitter_account = models.CharField(default=None, max_length=255)
    twitter_password = models.CharField(default=None, max_length=255)
    summary_reporting_email = models.EmailField(default='prime-minister@gmail.com')