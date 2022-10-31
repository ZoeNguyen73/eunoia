from django.urls import path

from .views import TimeslotListCreateViewSet

app_name = 'timeslots'

urlpatterns = [
  path('', TimeslotListCreateViewSet.as_view({'get': 'list', 'post': 'create'}), name='listing_timeslot'),
]