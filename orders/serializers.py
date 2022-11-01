from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = [
      'id',
      'date_created',
      'donor_org_name',
      'donor_org_id',
      'charity_org_name',
      'charity_org_id',
      'collection_date',
      'collection_timeslot',
      'collection_address_contact_name',
      'collection_address_contact_number',
      'collection_address_details',
      'collection_address_postal_code',
      'delivery_address_contact_name',
      'delivery_address_contact_number',
      'delivery_address_details',
      'delivery_address_postal_code',
      'completion_time',
      'need_delivery',
      'status',
    ]

class OrderUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    read_only_fields = (
      'id',
      'date_created',
      'donor_org_name',
      'donor_org_id',
      'charity_org_name',
      'charity_org_id',
      'collection_date',
      'collection_timeslot',
      'collection_address_contact_name',
      'collection_address_contact_number',
      'collection_address_details',
      'collection_address_postal_code',
      'delivery_address_contact_name',
      'delivery_address_contact_number',
      'delivery_address_details',
      'delivery_address_postal_code',
      'completion_time',
      'need_delivery',
    )
    fields = [
      'id',
      'date_created',
      'donor_org_name',
      'donor_org_id',
      'charity_org_name',
      'charity_org_id',
      'collection_date',
      'collection_timeslot',
      'collection_address_contact_name',
      'collection_address_contact_number',
      'collection_address_details',
      'collection_address_postal_code',
      'delivery_address_contact_name',
      'delivery_address_contact_number',
      'delivery_address_details',
      'delivery_address_postal_code',
      'completion_time',
      'need_delivery',
      'status',
    ]