from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Organization
from .serializers import OrganizationSerializer
from .permissions import IsOrganizationAdmin

# Create your views here.
class OrganizationViewSet(ModelViewSet):
  serializer_class = OrganizationSerializer
  queryset = Organization.objects.filter(status='active')
  lookup_field = 'slug'
  lookup_url_kwarg = 'slug'

  def get_permissions(self):
    if self.action in ['list', 'retrieve']:
      permission_classes = (AllowAny,)
    elif self.action == 'add':
      permission_classes = (IsAuthenticated,)
    else:
      permission_classes = (IsOrganizationAdmin,)
    return [permission() for permission in permission_classes]