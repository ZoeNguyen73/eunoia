from rest_framework import serializers

from .models import Order_Listing

class OrderListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order_Listing
    depth = 1
    fields = [
      'id', 
      'order', 
      'name',
      'description',
      'expiry_date',
      'image_url',
      ]