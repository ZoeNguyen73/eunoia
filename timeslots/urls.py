from django.urls import path

from .views import TimeslotListCreateViewSet, TimeslotDeleteView

app_name = 'timeslots'

urlpatterns = [
  path('<timeslot_id>', TimeslotDeleteView.as_view({'delete': 'destroy'}), name='listing_timeslot_delete'),
  path('', TimeslotListCreateViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='listing_timeslot'),
]