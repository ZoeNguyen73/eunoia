from django.urls import path

from .views import UserProfileImageUpdateView

app_name = 'users'

urlpatterns = [
  path('profile-image', UserProfileImageUpdateView.as_view({"patch": "partial_update"}), name="user_profile_image_update"),
]
