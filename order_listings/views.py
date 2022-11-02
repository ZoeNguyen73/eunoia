from hashlib import new
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order
from listings.models import Listing
from items.models import Item
from .models import Order_Listing
from .serializers import OrderListingSerializer

class OrderListingViewSet(ModelViewSet):
  serializer_class = OrderListingSerializer
  permission_classes = [IsAuthenticated,]

  def list(self, request, id):
    if request.user.organization is None:
      return Response(
        {'detail': 'You are not an admin of any organization'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    order = Order.objects.get(id=id)
    if order is None:
      return Response(
        {'detail': 'Order not found'},
        status=status.HTTP_404_NOT_FOUND
      )

    if str(request.user.organization) != str(order.charity_org_name) and str(request.user.organization) != str(order.donor_org_name):
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    
    queryset = Order_Listing.objects.filter(order=order)
    serializer = OrderListingSerializer(queryset, many=True)
    return Response(serializer.data)
  
  def create(self, request, id):
    if request.user.organization is None:
      return Response(
        {'detail': 'You are not an admin of any organization'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    order = Order.objects.get(id=id)
    if order is None:
      return Response(
        {'detail': 'Order not found'},
        status=status.HTTP_404_NOT_FOUND
      )

    if str(request.user.organization) != str(order.charity_org_name):
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    
    if request.user.organization.status != 'active':
      return Response(
        {'detail': 'Only active organizations can create new orders'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if request.user.organization.organization_type == 'Donor':
      return Response(
        {'detail': 'Donor organizations cannot create orders'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    listing = Listing.objects.get(id=request.data['listing_id'])
    if listing is None:
      return Response(
        {'detail': 'Listing cannot be found'},
        status=status.HTTP_404_NOT_FOUND
      )
    if listing.status != 'active':
      return Response(
        {'detail': 'Listing is no longer active'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if Order_Listing.objects.filter(listing_id=str(listing.id)).exists():
      existing_order_listings = Order_Listing.filter(listing_id=str(listing.id))
      for item in existing_order_listings:
        if item.order.status != 'cancelled':
          return Response(
            {'detail': 'Listing has already been added in an order'},
            status=status.HTTP_400_BAD_REQUEST
          )  

    request.data._mutable = True
    request.data['name'] = listing.item.name
    request.data['expiry_date'] = listing.expiry_date
    request.data['description'] = listing.item.description
    request.data['image_url'] = None if listing.item.image_url is None else listing.item.image_url
 
    request.data._mutable = False
    
    new_order_listing_data = super().create(request)
    new_order_listing = Order_Listing.objects.get(id=new_order_listing_data.data['id'])
    
    new_order_listing.order = order
    new_order_listing.save()

    listing.status = 'confirmed'
    listing.save()

    serializer = OrderListingSerializer(new_order_listing)
    return Response(serializer.data)