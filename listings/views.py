import uuid

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import get_object_or_404

from organizations.models import Organization
from items.models import Item
from addresses.models import Address
from .serializers import ListingSerializer
from .models import Listing
from utils.permissions import IsSuperUser

class ListingListCreateViewSet(ModelViewSet):
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
    
    if not self.is_valid_uuid(request.data['item']):
      return Response(
        {'detail': 'Item info is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    item = Item.objects.get(id=request.data['item'])
    if item is None or item.organization != organization:
      return Response(
        {'detail': 'Item info is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if not self.is_valid_uuid(request.data['collection_address']):
      return Response(
        {'detail': 'Address info is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    address = Address.objects.get(id=request.data['collection_address'])
    if address is None or address.organization != organization:
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

class ListingRetrieveUpdateDeleteViewSet(ModelViewSet):
  serializer_class = ListingSerializer
  permission_classes = [AllowAny,]
  lookup_field = 'id'
  lookup_url_kwarg = 'id'
  queryset = Listing.objects.all()

  @staticmethod
  def is_valid_uuid(val):
    try:
      uuid.UUID(str(val))
      return True
    except ValueError:
      return False

  def get_permissions(self):
    if self.action in ['retrieve']:
      permission_classes = (AllowAny,)
    else:
      permission_classes = (IsAuthenticated,)
    return [permission() for permission in permission_classes]

  def partial_update(self, request, id, *args, **kwargs):
    listing = Listing.objects.get(id=id);
    if request.user.organization != listing.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )

    if request.data['collection_address']:
      if not self.is_valid_uuid(request.data['collection_address']):
        return Response(
          {'detail': 'Address info is invalid'},
          status=status.HTTP_400_BAD_REQUEST
        )
    
      address = Address.objects.get(id=request.data['collection_address'])
      if address is None or address.organization != listing.organization:
        return Response(
          {'detail': 'Address info is invalid'},
          status=status.HTTP_400_BAD_REQUEST
        )
      
      listing.collection_address = address
      listing.save()

    return super().partial_update(request, *args, **kwargs)
  
  def destroy(self, request, id):
    listing = Listing.objects.get(id=id)
    if request.user.organization != listing.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    return super().destroy(request)
    