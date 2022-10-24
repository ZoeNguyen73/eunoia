from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from .models import User
from .serializers import UserSerializer, UserProfileImageSerializer, UserPasswordSerializer
from .permissions import IsAccountOwner
from utils.imagekit import upload_file, delete_file
from eunoia.settings import BACKEND_URL

# Create your views here.
class UserActivateView(ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  http_method_names = ['patch', ]
  permission_classes = [AllowAny,]
  
  def partial_update(self, request, token):
    if User.objects.filter(activation_token=token, is_active=False).exists():
      user = User.objects.get(activation_token=token, is_active=False)
      user.is_active=True
      user.activation_token=''
      user.save()
      return Response(
        {'detail': 'User {} is successfully activated.'.format(user.username)},
        status=status.HTTP_200_OK
      )
    else:
      return Response(
        {'detail': 'User cannot be activated.'},
        status=status.HTTP_400_BAD_REQUEST
      )

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
    request.data._mutable = True
    profile_image_file = request.data.pop('profile_image', None)

    if profile_image_file:
      image_upload = upload_file(profile_image_file[0], 'profile_image')
      request.data.__setitem__('profile_image', image_upload['url'])
      request.data.__setitem__('profile_image_id', image_upload['id'])

    activation_token = get_random_string(length=32)
    verify_link = BACKEND_URL + '/users/activate/' + activation_token

    recipient = request.data['email']
    message = 'Please click on this link {} to verify your email and activate your account.'.format(verify_link)

    send_mail(
      'Verify your email to activate',
      message,
      'eunoia.singapore@gmail.com',
      [recipient],
      fail_silently=False
    )

    request.data['activation_token'] = activation_token
    request.data._mutable = False

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