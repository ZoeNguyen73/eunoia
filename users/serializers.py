from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  class Meta:
    model = User
    fields = [
      'id',
      'username',
      'email',
      'password',
      'profile_image',
      'organization',
      'contact_number',
      'is_superuser',
    ]
  
  def create(self, validated_data):
    return User.objects.create_user(**validated_data)