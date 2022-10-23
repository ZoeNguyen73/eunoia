# from django.core.paginator import Paginator
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.settings import api_settings

from base64 import b64encode
from collections import namedtuple
from urllib import parse

from .models import Organization

class OrganizationSerializer(ModelSerializer):
  # organizations = SerializerMethodField('get_paginated_organizations')

  class Meta:
    model = Organization
    fields = [
      'id',
      'name',
      'description',
      'website',
      'email',
      'organization_type',
      'status',
      'logo_url',
    ]
  
  # def create(self, validated_data):
  #   return Organization.objects.create_organization(**validated_data)
  
  # def get_paginated_organizations(self, obj):
  #   page_size = api_settings.PAGE_SIZE
  #   organizations = obj.organizations.all()
  #   paginator = Paginator(organizations, page_size)
  #   paginated_organizations = paginator.page(1)
  #   serializer = 