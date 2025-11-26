from django.contrib import admin
from .models import (
        Operator,
        Crisis,
        CrisisType,
        CrisisAssistance,
        SiteSettings,
        EmergencyAgencies,
        SocialMediaAccount
        )

admin.site.register(Operator)
'''
    Call the django default admin page to handel the models we have in admin panel
'''
class CrisisAdmin(admin.ModelAdmin):
    list_display = ('crisis_id', 'crisis_description','crisis_time','visible')
    list_editable = ('visible',)
admin.site.register(Crisis, CrisisAdmin)
admin.site.register(CrisisType)
admin.site.register(CrisisAssistance)
admin.site.register(SiteSettings)
admin.site.register(EmergencyAgencies)
admin.site.register(SocialMediaAccount)