from django.urls import path

from .views import OrganizationAdminUpdateView, OrganizationStatusUpdateView

app_name = 'organizations'

urlpatterns = [
  path('admins/<username>/<action_type>/', OrganizationAdminUpdateView.as_view({"patch": "partial_update"}), name='organization_admin_update'),
  path('admins/', OrganizationAdminUpdateView.as_view({"get": "get_admins"}), name='organization_admins'),
  path('status/<action_type>/', OrganizationStatusUpdateView.as_view({"patch": "partial_update"}), name='organization_status_update'),
]