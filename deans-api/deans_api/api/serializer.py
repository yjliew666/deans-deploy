from .models import (
    Crisis,
    CrisisAssistance,
    CrisisType,
    SiteSettings,
    EmergencyAgencies
    )
from rest_framework import serializers
from django.utils.timezone import now
from .models.Crisis import STATUS_CHOICES
from django.contrib.auth.models import User

'''This file contains all the serializers the api is using.
    Each model will be serialized in a way that can be processed and inside a json format.
'''

class CrisisAssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisAssistance
        fields = ('id','name',)

class CrisisTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisType
        fields = ('id','name',)

class CrisisSerializer(serializers.ModelSerializer):
    crisis_type = serializers.PrimaryKeyRelatedField(many=True, queryset=CrisisType.objects.all())
    crisis_assistance = serializers.PrimaryKeyRelatedField(many=True, queryset=CrisisAssistance.objects.all())
    class Meta:
        model = Crisis
        fields = (
                    'crisis_id',
                    'your_name',
                    'mobile_number',
                    'crisis_type',
                    'crisis_description',
                    'crisis_assistance',
                    'crisis_assistance_description',
                    'crisis_status',
                    'crisis_time',
                    'crisis_location1',
                    'crisis_location2',
                    'phone_number_to_notify'
                )
                
class CrisisBasicSerializer(serializers.ModelSerializer):
    crisis_type = serializers.PrimaryKeyRelatedField(many=True, queryset=CrisisType.objects.all())
    crisis_assistance = serializers.PrimaryKeyRelatedField(many=True, queryset=CrisisAssistance.objects.all())
    class Meta:
        model = Crisis
        fields = (
                    'crisis_id',
                    'your_name',
                    'mobile_number',
                    'crisis_type',
                    'crisis_description',
                    'crisis_assistance',
                    'crisis_assistance_description',
                    'crisis_status',
                    'crisis_time',
                    'crisis_location1',
                    'crisis_location2'
                )

class CrisisUpdateSerializer(serializers.ModelSerializer):
    # content = serializers.CharField(required=True)
    # thread = serializers.HyperlinkedRelatedField(
    #     read_only=True,
    #     view_name='thread-detail'
    # )
    # creator = serializers.HyperlinkedRelatedField(
    #     read_only=True,
    #     view_name='user-detail',
    #     lookup_field='username'
    # )
    class Meta:
        model = Crisis
        fields = (
            'crisis_type',
            'your_name',
            'mobile_number',
            'crisis_description',
            'crisis_assistance',
            'crisis_assistance_description',
            'crisis_status',
            'crisis_location1',
            'crisis_location2'
        )

    def update(self, instance, validated_data):
        # Update fields if there is any change
        for field, value in validated_data.items():
            setattr(instance, field, value)
        # Update 'updated_at' field to now
        setattr(instance, 'updated_at', now())

        # Note: If user update post, it won't change the last_activity
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username']
        )
        user.is_staff = validated_data['is_staff']
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'is_staff')

class UserAdminSerializer(UserSerializer):
    def update(self, instance, validated_data):
        if "is_staff" in validated_data:
            instance.is_staff = validated_data['is_staff']
        if "password" in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_staff')

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = (
            'facebook_account',
            'facebook_password',
            'twitter_account',
            'twitter_password',
            'summary_reporting_email',
        )

class EmergencyAgenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAgencies
        fields = (
            'agency_id',
            'agency',
            'phone_number'
        )

class EmergencyAgenciesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAgencies
        fields = (
            'agency_id',
            'agency',
            'phone_number'
        )

    # def update(self, instance, validated_data):
    #     # Update fields if there is any change
    #     for field, value in validated_data.items():
    #         setattr(instance, field, value)
    #     # Update 'updated_at' field to now
    #     setattr(instance, 'updated_at', now())
    #
    #     # Note: If user update post, it won't change the last_activity
    #     instance.save()
    #     return instance