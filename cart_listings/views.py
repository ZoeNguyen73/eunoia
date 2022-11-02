from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from organizations.models import Organization
from carts.models import Cart
from listings.models import Listing
from .serializers import CartListingSerializer
from .models import Cart_Listing

class CartListingViewSet(ModelViewSet):
  serializer_class = CartListingSerializer
  permission_classes = [IsAuthenticated,]

  def list(self, request):
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
    cart = Cart.objects.get(organization=organization)
    if cart is None:
      return Response(
        {'detail': 'Cart cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )
    
    queryset = Cart_Listing.objects.filter(cart=cart)
    serializer = CartListingSerializer(queryset, many=True)
    return Response(serializer.data)

class CartListingUpdateViewSet(ModelViewSet):
  serializer_class = CartListingSerializer
  permission_classes = [IsAuthenticated,]

  def create(self, request, listing_id):
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
    cart = Cart.objects.get(organization=organization)
    if cart is None:
      return Response(
        {'detail': 'Cart cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )
    
    listing = Listing.objects.get(id=listing_id)
    if listing is None:
      return Response(
        {'detail': 'Listing cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )
    if listing.status != 'active':
      return Response(
        {'detail': 'Listing is currently {}'.format(listing.status)},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if Cart_Listing.objects.filter(cart=cart, listing=listing).exists():
      return Response(
        {'detail': 'Listing is already added to cart'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    new_cart_listing_data = super().create(request)
    new_cart_listing = Cart_Listing.objects.get(id=new_cart_listing_data.data['id'])

    new_cart_listing.cart = cart
    new_cart_listing.listing = listing

    new_cart_listing.save()

    serializer = CartListingSerializer(new_cart_listing)

    return Response(serializer.data)
  
  def destroy(self, request, listing_id):
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
    cart = Cart.objects.get(organization=organization)
    if cart is None:
      return Response(
        {'detail': 'Cart cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )
    
    listing = Listing.objects.get(id=listing_id)
    if listing is None:
      return Response(
        {'detail': 'Listing cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )

    if not Cart_Listing.objects.filter(cart=cart, listing=listing).exists():
      return Response(
        {'detail': 'Listing has not been added to cart'},
        status=status.HTTP_404_NOT_FOUND
      )
    
    cart_listing = Cart_Listing.objects.get(cart=cart, listing=listing)
    cart_listing.delete()

    return Response(
      {'detail': 'Listing successfully removed from cart'},
      status=status.HTTP_200_OK
    )
