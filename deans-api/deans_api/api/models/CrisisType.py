from django.db.models import Model, CharField
'''
    CrisisType model, carries the name of the crisisType only
'''
class CrisisType (Model):
    name=CharField(
            default=None,
            max_length=(255))

    def __str__(self):
        return self.name

    class Meta:
        pass