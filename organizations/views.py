from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Organization
from .serializers import OrganizationSerializer, OrganizationAdminSerializer, OrganizationStatusSerializer, OrganizationLogoSerializer
from .permissions import IsOrganizationAdmin

from users.models import User
from users.serializers import UserSerializer
from utils.permissions import IsSuperUser
from carts.models import Cart
from listings.models import Listing
from cart_listings.models import Cart_Listing

from utils.imagekit import upload_file, delete_file

class OrganizationViewSet(ModelViewSet):
  serializer_class = OrganizationSerializer
  queryset = Organization.objects.filter(status='active')
  lookup_field = 'slug'
  lookup_url_kwarg = 'slug'

  def get_permissions(self):
    if self.action in ['list', 'retrieve']:
      permission_classes = (AllowAny,)
    elif self.action in ['add', 'create']:
      permission_classes = (IsAuthenticated,)
    else:
      permission_classes = (IsOrganizationAdmin,)
    return [permission() for permission in permission_classes]

  def create(self, request, *args, **kwargs):
    if request.user.organization != None:
      return Response(
        {'detail': 'User is already an admin of another organization'},
        status=status.HTTP_409_CONFLICT
      )

    request.data._mutable = True
    logo_file = request.data.pop('logo_image', None)

    if logo_file and logo_file[0] != '':
      logo_upload = upload_file(logo_file[0], 'logo_image')
      request.data.__setitem__('logo_url', logo_upload['url'])
      request.data.__setitem__('logo_id', logo_upload['id'])

    request.data._mutable = False
    new_organization_data = super().create(request, *args, **kwargs)
    created_org = Organization.objects.get(id=new_organization_data.data['id'])

    request.user.organization = created_org
    request.user.save()

    return new_organization_data
  
  @staticmethod
  def update_logo(current_logo_id, file, file_name):
    if current_logo_id:
      delete_file(current_logo_id)
    
    return upload_file(file, file_name)
  
  def partial_update(self, request, slug, *args, **kwargs):
    organization_object = Organization.objects.get(slug=slug)
    organization = OrganizationLogoSerializer(organization_object).data

    request.data._mutable = True
    logo_file = request.data.pop('logo_image', None)
    current_logo_id = None if organization.get('logo_id') == '' else organization.get('logo_id')
    print('current logo id', current_logo_id)

    if logo_file and logo_file[0] != '':
      new_logo_image = self.update_logo(current_logo_id, logo_file[0], 'logo_image')
      request.data.__setitem__('logo_url', new_logo_image['url'])
      request.data.__setitem__('logo_id', new_logo_image['id'])
      request.data._mutable = False
      return super().partial_update(request, *args, **kwargs)
      
    request.data._mutable = False
    return super().partial_update(request, *args, **kwargs)

class OrganizationViewByTypeSet(ViewSet):
  http_method_names = ['get', ]
  permission_classes = [AllowAny,]
  queryset = Organization.objects.filter(status='active')

  def list(self, request, type):
    if type == 'donors':
      queryset = Organization.objects.filter(status='active', organization_type='Donor')
    elif type == 'charities':
      queryset = Organization.objects.filter(status='active', organization_type='Charity')
    else:
      queryset = Organization.objects.filter(status='active')
    serializer = OrganizationSerializer(queryset, many=True)
    return Response(serializer.data) 

class OrganizationAdminUpdateView(ModelViewSet):
  serializer_class = OrganizationAdminSerializer
  queryset = Organization.objects.all()
  lookup_field = 'slug'
  lookup_url_kwarg = 'slug'
  permission_classes = [IsAuthenticated, IsOrganizationAdmin,]
  http_method_names = ['patch', 'get']

  def get_admins(self, request, slug):
    organization = Organization.objects.get(slug=slug)
    users = UserSerializer(User.objects.filter(organization=organization), many=True)
    return Response(users.data)

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
        {'detail': 'Organization {} is successfully activated.'.format(organization.name)},
        status=status.HTTP_200_OK
      )

    elif action_type == 'deactivate':
      organization.status = 'deactivated'
      organization.save()

      if Cart.objects.filter(organization=organization).exists():
        cart = Cart.objects.get(organization=organization)
        cart.delete()

      if Listing.objects.filter(organization=organization).exists():
        listings = Listing.objects.filter(organization=organization)
        for listing in listings:
          listing.status = 'inactive'
          listing.save()
          if Cart_Listing.objects.filter(listing=listing).exists():
            cart_listings = Cart_Listing.objects.filter(listing=listing)
            for cart_listing in cart_listings:
              cart_listing.delete()  

      return Response(
        {'detail': 'Organization {} is successfully deactivated.'.format(organization.name)},
        status=status.HTTP_200_OK
      )