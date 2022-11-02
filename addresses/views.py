from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Address
from .serializers import AddressSerializer
from .permissions import IsOrganizationAdmin, IsSuperUser

from organizations.models import Organization

class AddressViewSet(ModelViewSet):
  serializer_class = AddressSerializer

  def get_permissions(self):
    if self.action in ['list', 'retrieve',]:
      permission_classes = (AllowAny,)
    elif self.action in ['create', 'update', 'partial_update', 'delete']:
      permission_classes = [IsAuthenticated, IsOrganizationAdmin,]
    else:
      permission_classes = (IsSuperUser,)
    return [permission() for permission in permission_classes]

  def list(self, request, slug):
    organization = Organization.objects.get(slug=slug)
    queryset = Address.objects.filter(organization=organization)
    serializer = AddressSerializer(queryset, many=True)
    return Response(serializer.data)
  
  def create(self, request, slug, *args, **kwargs):
    organization = Organization.objects.get(slug=slug)
    if organization.status != 'active':
      return Response(
        {'detail': 'Only active organization can create addresses'},
        status=status.HTTP_400_BAD_REQUEST
      )
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    request.data._mutable = True
    request.data['organization'] = organization.id
    request.data._mutable = False
    return super().create(request, *args, **kwargs)

class AddressRetrieveViewSet(ModelViewSet):
  serializer_class = AddressSerializer
  lookup_field = 'id'
  lookup_url_kwarg = 'id'
  queryset = Address.objects.all()

  def retrieve(self, request, slug, id):
    organization = Organization.objects.get(slug=slug)
    queryset = Address.objects.filter(organization=organization)
    address = get_object_or_404(queryset, id=id)
    serializer = AddressSerializer(address)
    return Response(serializer.data)
  
  def destroy(self, request, slug, id):
    organization = Organization.objects.get(slug=slug)
    if organization.status != 'active':
      return Response(
        {'detail': 'Organization status is not active'},
        status=status.HTTP_400_BAD_REQUEST
      )
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    return super().destroy(request)
  
  def partial_update(self, request, slug, id, *args, **kwargs):
    organization = Organization.objects.get(slug=slug)
    if organization.status != 'active':
      return Response(
        {'detail': 'Organization status is not active'},
        status=status.HTTP_400_BAD_REQUEST
      )
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    return super().partial_update(request, *args, **kwargs)

class AddressDefaultUpdateSet(ModelViewSet):
  serializer_class = AddressSerializer
  lookup_field = 'id'
  lookup_url_kwarg = 'id'
  queryset = Address.objects.all()

  def partial_update(self, request, slug, id):
    organization = Organization.objects.get(slug=slug)
    if organization.status != 'active':
      return Response(
        {'detail': 'Organization status is not active'},
        status=status.HTTP_400_BAD_REQUEST
      )
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    queryset = Address.objects.filter(organization=organization, is_default=True)
    q = queryset.exclude(id=id)
    if q.count() > 0:
      for a in q:
        a.is_default = False
        a.save()

    address = Address.objects.get(id=id)
    address.is_default = True
    address.save()
    return Response(
      {'detail': 'Default address updated successfully'},
      status=status.HTTP_200_OK
    )
