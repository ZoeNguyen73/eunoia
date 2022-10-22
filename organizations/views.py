from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Organization
from .serializers import OrganizationSerializer

# Create your views here.
class OrganizationViewSet(ModelViewSet):
  serializer_class = OrganizationSerializer
  queryset = Organization.objects.filter(status='active')
  lookup_field = 'slug'
  lookup_url_kwarg = 'slug'