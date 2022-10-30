from rest_framework import serializers

from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Listing
    depth = 1
    fields = [
      'id',
      'item',
      'collection_address',
      'organization',
      'status',
      'expiry_date',
      'collection_time',
      'date_created',
    ]

class ListingUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Listing
    depth = 1
    read_only_fields = ('item', 'organization')
    fields = [
      'id',
      'item',
      'collection_address',
      'organization',
      'status',
      'expiry_date',
      'collection_time',
      'date_created',
    ]