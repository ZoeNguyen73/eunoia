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

  # def get_queryset(self):
  #   queryset = Organization.objects.filter(status='active')
  #   # slug = self.kwargs['slug']
  #   # if slug is not None:
  #   #   queryset = queryset.filter(slug=slug)
  #   return queryset

  # def list(self, request):
  #   queryset = Organization.objects.filter(status='ACTIVE')
  #   serializer = OrganizationSerializer(queryset, many=True)
  #   return Response(serializer.data)
  
  # def retrieve(self, request, pk=None):
  #   queryset = Organization.objects.all()
  #   organization = get_object_or_404(queryset, pk=pk)
  #   serializer = OrganizationSerializer(organization)
  #   return Response(serializer.data)