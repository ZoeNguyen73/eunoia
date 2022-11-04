from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from utils.imagekit import upload_file, delete_file

from organizations.models import Organization
from .serializers import ItemSerializer
from .models import Item

class ItemViewSet(ModelViewSet):
  serializer_class = ItemSerializer
  permission_classes = [IsAuthenticated,]

  def list(self, request, slug):
    if request.user.organization is None:
      return Response(
        {'detail': 'You are not an admin of any organization'},
        status=status.HTTP_400_BAD_REQUEST
      )
    organization = Organization.objects.get(slug=slug)
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    queryset = Item.objects.filter(organization=organization)
    serializer = ItemSerializer(queryset, many=True)
    return Response(serializer.data)

  def create(self, request, slug, *args, **kwargs):
    organization = Organization.objects.get(slug=slug)
    if organization.organization_type == 'Charity':
      return Response(
        {'detail': 'Charity organizations cannot create item'},
        status=status.HTTP_400_BAD_REQUEST
      )
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    if organization.status != 'active':
      return Response(
        {'detail': 'Only active organization can create items'},
        status=status.HTTP_400_BAD_REQUEST
      )
    request.data._mutable = True
    request.data['organization'] = organization.id

    image_file = request.data.pop('image', None)

    if image_file and image_file[0] != '':
      image_upload = upload_file(image_file[0], 'item_image')
      request.data.__setitem__('image_url', image_upload['url'])
      request.data.__setitem__('image_id', image_upload['id'])

    request.data._mutable = False
    return super().create(request, *args, **kwargs)


class ItemRetrieveViewSet(ModelViewSet):
  serializer_class = ItemSerializer
  permission_classes = [IsAuthenticated,]
  lookup_field = 'id'
  lookup_url_kwarg = 'id'
  queryset = Item.objects.all()

  @staticmethod
  def update_image(current_image_id, file, file_name):
    if current_image_id:
      delete_file(current_image_id)
    
    return upload_file(file, file_name)

  def retrieve(self, request, slug, id):
    organization = Organization.objects.get(slug=slug)
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    queryset = Item.objects.filter(organization=organization)
    item = get_object_or_404(queryset, id=id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)
  
  def destroy(self, request, slug, id):
    organization = Organization.objects.get(slug=slug)
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    if organization.status != 'active':
      return Response(
        {'detail': 'Only active organization can make changes to items'},
        status=status.HTTP_400_BAD_REQUEST
      )
    return super().destroy(request)
  
  def partial_update(self, request, slug, id, *args, **kwargs):
    organization = Organization.objects.get(slug=slug)
    if organization != request.user.organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    if organization.status != 'active':
      return Response(
        {'detail': 'Only active organization can make changes to items'},
        status=status.HTTP_400_BAD_REQUEST
      )
    item = Item.objects.get(id=id)
    request.data._mutable = True
    image_file = request.data.pop('image', None)
    current_image_id = None if item.image_id == '' else item.image_id

    if image_file and image_file[0] != '':
      new_image_upload = self.update_image(current_image_id, image_file[0], 'item_image')
      request.data.__setitem__('image_url', new_image_upload['url'])
      request.data.__setitem__('image_id', new_image_upload['id'])
      request.data._mutable = False
      return super().partial_update(request, *args, **kwargs)

    request.data._mutable = False
    return super().partial_update(request, *args, **kwargs)