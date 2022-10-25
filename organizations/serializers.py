# from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.settings import api_settings

from base64 import b64encode
from collections import namedtuple
from urllib import parse

from .models import Organization
from users.models import User

class OrganizationSerializer(serializers.ModelSerializer):
  # organizations = SerializerMethodField('get_paginated_organizations')
  logo_id = serializers.CharField(required=False, write_only=True)

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
      'slug',
      'logo_url',
      'logo_id',
    ]
  
  # def create(self, validated_data):
  #   return Organization.objects.create_organization(**validated_data)
  
  # def get_paginated_organizations(self, obj):
  #   page_size = api_settings.PAGE_SIZE
  #   organizations = obj.organizations.all()
  #   paginator = Paginator(organizations, page_size)
  #   paginated_organizations = paginator.page(1)
  #   serializer = 

class OrganizationAdminSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [ 'organization' ]

class OrganizationStatusSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = [ 'status' ]

class OrganizationLogoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = ['logo_url', 'logo_id']