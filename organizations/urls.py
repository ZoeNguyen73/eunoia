from django.urls import path

from .views import OrganizationAdminUpdateView

app_name = 'organizations'

urlpatterns = [
  path('admins/<username>/<action_type>/', OrganizationAdminUpdateView.as_view({"patch": "partial_update"}), name='organization_admin_add'),
  # path('admins/<username>/remove/', OrganizationAdminUpdateView.as_view({"patch": "partial_update"}), name='organization_admin_remove'),
]