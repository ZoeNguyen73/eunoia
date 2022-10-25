from rest_framework import serializers

from .models import Address

class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = [
      'id',
      'name',
      'contact_name',
      'contact_number',
      'details',
      'postal_code',
      'organization',
      'is_default',
    ]