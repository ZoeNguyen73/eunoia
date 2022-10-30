from django.urls import path

from .views import ItemViewSet, ItemRetrieveViewSet

app_name = 'items'

urlpatterns = [
  path('', ItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='organization_items'),
  path('<id>', ItemRetrieveViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='organization_items_retrieve'),
]