from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect

from .models import User
from .serializers import UserSerializer, UserProfileImageSerializer, UserPasswordSerializer
from .permissions import IsAccountOwner
from utils.imagekit import upload_file, delete_file

# Create your views here.
class UserViewSet(ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  lookup_field = 'username'
  lookup_url_kwarg = 'username'

  def get_permissions(self):
    if self.action in ['list', 'retrieve', 'create']:
      permission_classes = (AllowAny,)
    elif self.action in ['update', 'partial_update', 'delete']:
      permission_classes = (IsAccountOwner,)
    else:
      permission_classes = (IsAuthenticated,)
    return [permission() for permission in permission_classes]
  
  def create(self, request, *args, **kwargs):
    profile_image_file = request.data.pop('profile_image', None)

    if profile_image_file:
      image_upload = upload_file(profile_image_file[0], 'profile_image')
      request.data.__setitem__('profile_image', image_upload['url'])
      request.data.__setitem__('profile_image_id', image_upload['id'])
    
    return super().create(request, *args, **kwargs)
  
  @staticmethod
  def update_profile_image(current_profile_image_id, file, file_name):
    if current_profile_image_id:
      delete_file(current_profile_image_id)
    
    return upload_file(file, file_name)
  
  def partial_update(self, request, *args, **kwargs):
    user_object = User.objects.get(username=self.request.user)
    user = UserProfileImageSerializer(user_object).data

    request.data._mutable = True
    profile_image_file = request.data.pop('profile_image', None)
    current_profile_image_id = None if user.get('profile_image_id') == '' else user.get('profile_image_id')

    if profile_image_file:
      new_profile_image = self.update_profile_image(current_profile_image_id, profile_image_file[0], 'profile_image')
      request.data.__setitem__('profile_image', new_profile_image['url'])
      request.data.__setitem__('profile_image_id', new_profile_image['id'])
      request.data._mutable = False
      return super().partial_update(request, *args, **kwargs)
      
    request.data._mutable = False
    return super().partial_update(request, *args, **kwargs)