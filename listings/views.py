import uuid
from xmlrpc.client import ResponseError

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import render

from organizations.models import Organization
from items.models import Item
from addresses.models import Address
from .serializers import ListingSerializer
from .models import Listing
from utils.permissions import IsSuperUser

class ListingViewSet(ModelViewSet):
  serializer_class = ListingSerializer

  @staticmethod
  def is_valid_uuid(val):
    try:
      uuid.UUID(str(val))
      return True
    except ValueError:
      return False

  def get_permissions(self):
    if self.action in ['list',]:
      permission_classes = (AllowAny,)
    elif self.action in ['create',]:
      permission_classes = [IsAuthenticated,]
    else:
      permission_classes = (IsSuperUser,)
    return [permission() for permission in permission_classes]
  
  def list(self, request):
    queryset = Listing.objects.all().exclude(status='inactive')
    serializer = ListingSerializer(queryset, many=True)
    return Response(serializer.data)
  
  def create(self, request, *args, **kwargs):
    if request.user.organization is None:
      return Response(
        {'detail': 'You are not an admin of any organization'},
        status=status.HTTP_400_BAD_REQUEST
      )
    organization = Organization.objects.get(name=request.user.organization)
    if organization.organization_type == 'Charity':
      return Response(
        {'detail': 'Charity organizations cannot create listing'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if not self.is_valid_uuid(request.data['item']) or Item.objects.get(id=request.data['item']) == None:
      return Response(
        {'detail': 'Item info is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if not self.is_valid_uuid(request.data['collection_address']) or Address.objects.get(id=request.data['collection_address']) == None:
      return Response(
        {'detail': 'Address info is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    new_listing_data = super().create(request, *args, **kwargs)
    new_listing = Listing.objects.get(id=new_listing_data.data['id'])

    new_listing.item = Item.objects.get(id=request.data['item'])
    new_listing.collection_address = Address.objects.get(id=request.data['collection_address'])
    new_listing.organization = organization
    new_listing.save()

    serializer = ListingSerializer(new_listing)

    return Response(serializer.data)