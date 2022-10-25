from pyexpat import model
from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  organization = serializers.CharField(read_only=True)
  is_superuser = serializers.BooleanField(read_only=True)
  profile_image_id = serializers.CharField(required=False, write_only=True)
  activation_token = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = [
      'id',
      'username',
      'email',
      'password',
      'profile_image',
      'profile_image_id',
      'organization',
      'contact_number',
      'is_superuser',
      'activation_token',
    ]
  
  def create(self, validated_data):
    return User.objects.create_user(**validated_data)

class UserProfileImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['profile_image', 'profile_image_id']

class UserPasswordSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['password']
  
  def update(self, instance, validated_data):
    instance.set_password(validated_data['password'])
    instance.save()
    return instance