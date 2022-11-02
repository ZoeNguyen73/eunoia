from django.urls import path

from .views import CartListingViewSet, CartListingUpdateViewSet

app_name = 'cart_listings'

urlpatterns = [
  path('', CartListingViewSet.as_view({'get': 'list'}), name='cart_listings_list'),
  path('<listing_id>', CartListingUpdateViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='cart_listings_update'),
]