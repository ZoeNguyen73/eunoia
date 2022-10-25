from django.urls import path

from .views import AddressViewSet, AddressRetrieveViewSet, AddressDefaultUpdateSet

app_name = 'addresses'

urlpatterns = [
  path('', AddressViewSet.as_view({"get": "list", "post": "create"}), name='organization_addresses'),
  path('<id>/default/', AddressDefaultUpdateSet.as_view({"patch": "partial_update"}), name='organization_addresses_set_default'),
  path('<id>', AddressRetrieveViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}), name='organization_addresses_retrieve'),
]