from hashlib import new
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order
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
    
    new_order_listing_data = super().create(request)
    new_order_listing = Order_Listing.objects.get(id=new_order_listing_data.data['id'])
    
    new_order_listing.order = order
    new_order_listing.save()

    serializer = OrderListingSerializer(new_order_listing)
    return Response(serializer.data)