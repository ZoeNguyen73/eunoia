from rest_framework import serializers

from .models import Cart_Listing

class CartListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cart_Listing
    depth = 2
    fields = ['id', 'listing', 'cart']