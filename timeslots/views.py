import uuid

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import render

from .models import Timeslot
from .serializers import TimeslotSerializer
from utils.permissions import IsSuperUser
from listings.models import Listing

class TimeslotListCreateViewSet(ModelViewSet):
  serializer_class = TimeslotSerializer
  lookup_field = 'timeslot_id'
  lookup_url_kwarg = 'timeslot_id'

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
    elif self.action in ['create', 'destroy']:
      permission_classes = [IsAuthenticated,]
    else:
      permission_classes = (IsSuperUser,)
    return [permission() for permission in permission_classes]
  
  def list(self, request, id):
    if not self.is_valid_uuid(id):
      return Response(
        {'detail': 'Listing id is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )

    listing = Listing.objects.get(id=id)
  
    if listing is None:
      return Response(
        {'detail': 'Listing id cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )
    
    queryset = Timeslot.objects.filter(listing=listing)
    serializer = TimeslotSerializer(queryset, many=True)
    return Response(serializer.data)
  
  def create(self, request, id, *args, **kwargs):
    if not self.is_valid_uuid(id):
      return Response(
        {'detail': 'Listing id is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )

    listing = Listing.objects.get(id=id)
    if listing is None:
      return Response(
        {'detail': 'Listing id cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )

    if listing.organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    
    if Timeslot.objects.filter(listing=listing, date=request.data['date'], timeslot_option=request.data['timeslot_option']).exists():
      return Response(
        {"detail": "Timeslot already exists in database"},
        status=status.HTTP_400_BAD_REQUEST
      )

    request.data._mutable = True
    request.data['listing'] = listing.id
    request.data._mutable = False

    return super().create(request, *args, **kwargs)


class TimeslotDeleteView(ModelViewSet):
  serializer_class = TimeslotSerializer
  permission_class = [AllowAny,]
  lookup_field = 'id'
  lookup_url_kwarg = 'timeslot_id'
  queryset = Timeslot.objects.all()

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
    elif self.action in ['create', 'destroy']:
      permission_classes = [IsAuthenticated,]
    else:
      permission_classes = (IsSuperUser,)
    return [permission() for permission in permission_classes]
  
  def destroy(self, request, id, timeslot_id):
    if not self.is_valid_uuid(id):
      return Response(
        {'detail': 'Listing id is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )

    listing = Listing.objects.get(id=id)
    if listing is None:
      return Response(
        {'detail': 'Listing id cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )

    if listing.organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    
    timeslot = Timeslot.objects.get(id=timeslot_id)
    if listing != timeslot.listing:
      return Response(
        {'detail': 'Listing id is invalid'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    return super().destroy(request)


