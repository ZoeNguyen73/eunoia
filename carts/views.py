from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Cart
from .serializers import CartSerializer
from organizations.models import Organization

class CartViewSet(ModelViewSet):
  serializer_class = CartSerializer
  permission_classes = [IsAuthenticated,]

  def create(self, request):
    if request.user.organization is None:
      return Response(
        {'detail': 'You are not an admin of any organization'},
        status=status.HTTP_400_BAD_REQUEST
      )
    organization = Organization.objects.get(name=request.user.organization)
    if organization.organization_type == 'Donor':
      return Response(
        {'detail': 'Donor organizations cannot create cart'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if Cart.objects.filter(organization=organization).exists():
      return Response(
        {'detail': 'Cart already exists'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    request.data['organization'] = organization.id

    return super().create(request)
  
  def retrieve(self, request):
    if request.user.organization is None:
      return Response(
        {'detail': 'You are not an admin of any organization'},
        status=status.HTTP_400_BAD_REQUEST
      )
    organization = Organization.objects.get(name=request.user.organization)
    queryset = Cart.objects.all()
    cart = get_object_or_404(queryset, organization=organization)
    serializer = CartSerializer(cart)
    return Response(serializer.data)