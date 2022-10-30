from django.urls import path

from .views import ListingListCreateViewSet, ListingRetrieveUpdateDeleteViewSet

app_name = 'listings'

urlpatterns = [
  path('', ListingListCreateViewSet.as_view({'get': 'list', 'post': 'create'}), name='listing_list_create'),
  path('<id>', ListingRetrieveUpdateDeleteViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='listing_retrieve_update_delete'),
]