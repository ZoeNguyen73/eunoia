from django.urls import path

from .views import ListingViewSet

app_name = 'listings'

urlpatterns = [
  path('', ListingViewSet.as_view({'get': 'list', 'post': 'create'}), name='listing_list_create'),
]