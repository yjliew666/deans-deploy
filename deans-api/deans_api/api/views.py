from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, mixins, generics
from django.contrib.auth.models import User
from .permissions import NotAllowed
from .models import Crisis, CrisisAssistance, CrisisType, SiteSettings, EmergencyAgencies
from .serializer import (
                CrisisSerializer, 
                CrisisAssistanceSerializer, 
                CrisisTypeSerializer, 
                CrisisUpdateSerializer, 
                CrisisBasicSerializer, 
                UserSerializer, 
                UserAdminSerializer,
                SiteSettingsSerializer,
                EmergencyAgenciesSerializer,
                EmergencyAgenciesUpdateSerializer
            )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

# import channels.layers
# from asgiref.sync import async_to_sync

'''
    The View Classes here implements the V-view in the MVC architecture.
    CrisisView, CrisisUpdateView, CrisisPartialUpdateView, 
    CrisisAssistanceView, CrisisTypeView, 
    UserView, UserPartialUpdateView,
    SiteSettingView,
    EmergencyView, EmergencyPartialUpdateView
    
    will all be handled by an api url in urls.py
'''

class CrisisViewSet(viewsets.ModelViewSet):
    """
        Return a list of all the existing crisis.
    """
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer
    # def get_serializer_class(self):
    #     if self.request.user.is_staff:
    #         return CrisisSerializer
    #     return CrisisBasicSerializer


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

class CrisisUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    '''
    Book update API, need to submit both `name` and `author_name` fields
    At the same time, or django will prevent to do update for field missing
    '''
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class CrisisPartialUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class CrisisAssistanceViewSet(viewsets.ModelViewSet):
    queryset = CrisisAssistance.objects.all()
    serializer_class = CrisisAssistanceSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class CrisisTypeViewSet(viewsets.ModelViewSet):
    queryset = CrisisType.objects.all()
    serializer_class = CrisisTypeSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def get_serializer_class(self):
    #     if self.request.user.is_staff:
    #         return UserAdminSerializer
    #     return UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAdminUser] 
        elif self.action == 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [NotAllowed]
        return [permission() for permission in permission_classes]

class UserPartialUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class SiteSettingViewSet(viewsets.ModelViewSet):

    serializer_class = SiteSettingsSerializer
    queryset = SiteSettings.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class EmergencyAgenciesView(viewsets.ModelViewSet):

    serializer_class = EmergencyAgenciesSerializer
    queryset = EmergencyAgencies.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class EmergencyAgenciesPartialUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):

    serializer_class = EmergencyAgenciesUpdateSerializer
    queryset = EmergencyAgencies.objects.all()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)