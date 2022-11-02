from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Order
from organizations.models import Organization
from .serializers import OrderSerializer, OrderUpdateSerializer, OrderStatusSerializer

class OrderListCreateViewSet(ModelViewSet):
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated,]

  def list(self, request, slug):
    if request.user.organization is None:
      return Response(
        {'detail': 'You are not an admin of any organization'},
        status=status.HTTP_400_BAD_REQUEST
      )
    organization = Organization.objects.get(slug=slug)
    if request.user.organization != organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    queryset = Order.objects.filter(charity_ord_id=organization.id)
    serializer = OrderSerializer(queryset, many=True)
    return Response(serializer.data)
  
  def create(self, request, slug, *args, **kwargs):
    if request.user.organization is None:
      return Response(
        {'detail': 'You are not an admin of any organization'},
        status=status.HTTP_400_BAD_REQUEST
      )
    organization = Organization.objects.get(slug=slug)
    if request.user.organization != organization:
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    
    if organization.status != 'active':
      return Response(
        {'detail': 'Only active organizations can create new orders'},
        status=status.HTTP_400_BAD_REQUEST
      )

    if organization.organization_type == 'Donor':
      return Response(
        {'detail': 'Donor organizations cannot create orders'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    donor_organization = Organization.objects.get(name=request.data['donor_org_name'])
    if donor_organization is None:
      return Response(
        {'detail': 'Donor organization cannot be found'},
        status=status.HTTP_400_BAD_REQUEST
      )
    if donor_organization.status != 'active':
      return Response(
        {'detail': 'Donor organization is not active'},
        status=status.HTTP_400_BAD_REQUEST
      )
    if donor_organization.organization_type != 'Donor':
      return Response(
        {'detail': 'Invalid donor organization type'},
        status=status.HTTP_400_BAD_REQUEST
      )

    request.data._mutable = True
    
    request.data['charity_org_name'] = organization.name
    request.data['charity_org_id'] = str(organization.id)

    request.data._mutable = False
    
    return super().create(request, *args, **kwargs)

class OrderRetrieveUpdateViewSet(ModelViewSet):
  serializer_class = OrderUpdateSerializer
  permission_classes = [IsAuthenticated,]
  lookup_field = 'id'
  lookup_url_kwarg = 'id'
  queryset = Order.objects.all()

  def retrieve(self, request, id):
    queryset = Order.objects.all()
    order = get_object_or_404(queryset, id=id)

    if str(request.user.organization) != str(order.charity_org_name) and str(request.user.organization) != str(order.donor_org_name):
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    serializer = OrderUpdateSerializer(order)
    return Response(serializer.data)

  def partial_update(self, request, id):
    order = Order.objects.get(id=id)
    if str(request.user.organization) != str(order.charity_org_name) and str(request.user.organization) != str(order.donor_org_name):
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    if order.status != 'open':
      return Response(
        {"detail": "Only open orders can be edited"},
        status=status.HTTP_400_BAD_REQUEST
      )
    return super().partial_update(request)

class OrderStatusViewSet(ModelViewSet):
  serializer_class = OrderStatusSerializer
  permission_classes = [IsAuthenticated,]
  lookup_field = 'id'
  lookup_url_kwarg = 'id'
  queryset = Order.objects.all()

  def partial_update(self, request, id, action):
    order = Order.objects.get(id=id)
    if str(request.user.organization) != str(order.charity_org_name) and str(request.user.organization) != str(order.donor_org_name):
      return Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN
      )
    
    if order.status != 'open':
      return Response(
        {"detail": "Only open orders can be edited"},
        status=status.HTTP_400_BAD_REQUEST
      )

    if action == 'complete':
      if str(request.user.organization) != str(order.charity_org_name):
        return Response(
          {"detail": "Only charity organization can verify that order has been completed"},
          status=status.HTTP_403_FORBIDDEN
        )
      order.status = 'completed'
      order.save()
      return Response(
        {'detail': 'Order status is successfully changed to completed'},
        status=status.HTTP_200_OK
      )
    
    if action == 'cancel':
      order.status = 'cancelled'
      order.save()
      return Response(
        {'detail': 'Order status is successfully changed to cancelled'},
        status=status.HTTP_200_OK
      )

    return Response(
      {'detail': 'Unable to update order status'},
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )