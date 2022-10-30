from rest_framework import serializers

from .models import Item

class ItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = [
      'id',
      'name',
      'description',
      'item_type',
      'organization',
      'image_url',
      'image_id',
      'date_created',
    ]