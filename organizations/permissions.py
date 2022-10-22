from rest_framework.permissions import BasePermission

from users.models import User

class IsOrganizationAdmin(BasePermission):
  def has_object_permission(self, request, view, obj):
    user_found = User.objects.get(username == request.user)
    # print('user under permission', user.organization)
    return request.user.organization == user_found.organization
