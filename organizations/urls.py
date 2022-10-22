from django.urls import path
from . import views

urlpatterns = [
  path("", views.ListOrganizations, name="artist_list"),
]