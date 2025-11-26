from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers

from .views import (
    CrisisViewSet,
    CrisisAssistanceViewSet,
    CrisisTypeViewSet,
    CrisisUpdateView,
    CrisisPartialUpdateView,
    UserViewSet,
    UserPartialUpdateView,
    EmergencyAgenciesView,
    EmergencyAgenciesPartialUpdateView,
    SiteSettingViewSet
)
'''
    The Url Router here has dispatched all views in views.py to corresponding url.
    Api urls:
        /crises/
        /crises/update/pk
        /crises/update-partial/pk
        /crisisassistance/
        /crisistype/
        /users/
        /users/
        /emergencyagencies/
        /emergencyagencies/update-partial/pk
        /sitesettings/
'''
router = routers.DefaultRouter()
router.register(r'^crises', CrisisViewSet)
router.register(r'^crisisassistance', CrisisAssistanceViewSet)
router.register(r'^crisistype', CrisisTypeViewSet)
router.register(r'^users', UserViewSet)
router.register(r'^emergencyagencies', EmergencyAgenciesView)
router.register(r'^sitesettings', SiteSettingViewSet)


urlpatterns = [
	path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    url(r'^', include(router.urls)),
    # url(r'^crises/update/<int:pk>/edit/$', CrisisUpdateAPIView.as_view(), name='crisis-update')
    url(r'^crises/update/(?P<pk>\d+)/$', CrisisUpdateView.as_view(), name='crisis_update'),
    url(r'^crises/update-partial/(?P<pk>\d+)/$', CrisisPartialUpdateView.as_view(), name='crisis_partial_update'),
    url(r'^users/update-partial/(?P<pk>\d+)/$', UserPartialUpdateView.as_view(), name='user_partial_update'),
    url(r'^emergencyagencies/update-partial/(?P<pk>\d+)/$', EmergencyAgenciesPartialUpdateView.as_view(), name='emergencyagency_partial_update'),
]
# Registration with rest auth:
# url(r'^rest-auth/', include('rest_auth.urls')),
# url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),