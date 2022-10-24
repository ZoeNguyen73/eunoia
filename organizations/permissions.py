from rest_framework.permissions import BasePermission

from users.models import User

class IsOrganizationAdmin(BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj == request.user.organization
