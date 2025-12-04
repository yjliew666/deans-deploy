import logging
from typing import Dict, Any

from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers

from .models import (
  Crisis,
  CrisisAssistance,
  CrisisType,
  SiteSettings,
  EmergencyAgencies
)

# Initialize Logger
logger = logging.getLogger(__name__)

class CrisisAssistanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = CrisisAssistance
    fields = ('id', 'name',)


class CrisisTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = CrisisType
    fields = ('id', 'name',)

class BaseCrisisSerializer(serializers.ModelSerializer):
  """
  Base serializer containing common fields and configurations for Crisis models
  to avoid repetition across specific implementations.
  """
  crisis_type = serializers.PrimaryKeyRelatedField(
      many=True, queryset=CrisisType.objects.all()
  )
  crisis_assistance = serializers.PrimaryKeyRelatedField(
      many=True, queryset=CrisisAssistance.objects.all()
  )

  class Meta:
    model = Crisis
    fields = [
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
    ]


class CrisisSerializer(BaseCrisisSerializer):
  """
  Full serializer including sensitive or internal fields (e.g. phone_number_to_notify).
  """

  class Meta(BaseCrisisSerializer.Meta):
    # Extend the base fields list
    fields = BaseCrisisSerializer.Meta.fields + ['phone_number_to_notify']


class CrisisBasicSerializer(BaseCrisisSerializer):
  """
  Public-facing serializer (uses exactly the base fields).
  """
  pass


class CrisisUpdateSerializer(BaseCrisisSerializer):
  """
  Serializer specifically for handling updates to Crisis objects.
  """

  class Meta(BaseCrisisSerializer.Meta):
    # We might want to restrict fields here if necessary,
    # but currently it matches the base list.
    pass

  def update(self, instance: Crisis, validated_data: Dict[str, Any]) -> Crisis:
    """
    Updates the crisis instance and auto-updates the 'updated_at' timestamp.
    """
    # Inject the timestamp into data before calling super
    validated_data['updated_at'] = now()

    logger.info(
      f"Updating Crisis ID {instance.pk} - Status: {validated_data.get('crisis_status', instance.crisis_status)}")

    return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ('username', 'password', 'is_staff')

  def create(self, validated_data: Dict[str, Any]) -> User:
    try:
      user = User.objects.create_user(
          username=validated_data['username']
      )
      user.is_staff = validated_data.get('is_staff', False)
      user.set_password(validated_data['password'])
      user.save()

      logger.info(f"New user created: {user.username} (Staff: {user.is_staff})")
      return user

    except Exception as e:
      logger.error(
        f"Failed to create user {validated_data.get('username')}: {str(e)}")
      raise e


class UserAdminSerializer(UserSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'password', 'is_staff')

  def update(self, instance: User, validated_data: Dict[str, Any]) -> User:
    # Handle password hashing if provided
    if "password" in validated_data:
      instance.set_password(validated_data.pop("password"))

    # Super update handles the rest (username, is_staff, etc)
    instance = super().update(instance, validated_data)

    logger.info(f"Admin updated user: {instance.username}")
    return instance

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