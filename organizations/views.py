from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Organization
from users.models import User
from .serializers import OrganizationSerializer, OrganizationAdminSerializer, OrganizationStatusSerializer
from .permissions import IsOrganizationAdmin, IsSuperUser

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

class OrganizationAdminUpdateView(ModelViewSet):
  serializer_class = OrganizationAdminSerializer
  queryset = Organization.objects.all()
  lookup_field = 'slug'
  lookup_url_kwarg = 'slug'
  permission_classes = [IsAuthenticated, IsOrganizationAdmin,]
  http_method_names = ['patch', ]

  def partial_update(self, request, username, action_type, *args, **kwargs):
    organization = self.get_object()
    admin_user = User.objects.get(username=username)

    if action_type == 'add':
      if admin_user.organization is not None:
        return Response(
          {'detail': 'User {} is already an admin for organization {}.'.format(admin_user.username, organization.name)},
          status=status.HTTP_400_BAD_REQUEST
        )
      admin_user.organization = organization
    elif action_type == 'remove':
      admin_user.organization = None

    admin_user.save()

    return Response(
      {'detail': 'User {} successfully {} as admin for organization {}.'.format(admin_user.username, action_type, organization.name)},
      status=status.HTTP_200_OK
    )

class OrganizationStatusUpdateView(ModelViewSet):
  serializer_class = OrganizationStatusSerializer
  queryset = Organization.objects.all()
  lookup_field = 'slug'
  lookup_url_kwarg = 'slug'
  permission_classes = [IsAuthenticated, IsSuperUser,]
  http_method_names = ['patch', ]

  def partial_update(self, request, action_type, *args, **kwargs):
    organization = self.get_object()

    if action_type == 'activate':
      organization.status = 'active'
      organization.save()
      return Response(
        {'Message': 'Organization {} is successfully activated.'.format(organization.name)},
        status=status.HTTP_200_OK
      )

    elif action_type == 'deactivate':
      organization.status = 'deactivated'
      organization.save()
      return Response(
        {'Message': 'Organization {} is successfully deactivated.'.format(organization.name)},
        status=status.HTTP_200_OK
      )