from django.contrib.auth.models import User 
from django.db import models
'''
    Operator implements a user model of django default model.
'''
class Operator(models.Model):
    # operator_id = models.IntegerField()
    # operator_password = models.CharField(max_length=20)
    # operator_name = models.CharField(max_length=30)
    # is_admin = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')


    def __str__(self):
        return self.operator_id

    class Meta:
        pass