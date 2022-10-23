from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserSerializer

# Create your views here.
class UserViewSet(ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  lookup_field = 'username'
  lookup_url_kwarg = 'username'

  def get_permissions(self):
    if self.action in ['list', 'retrieve', 'create']:
      permission_classes = (AllowAny,)
    else:
      permission_classes = (IsAuthenticated,)
    return [permission() for permission in permission_classes]