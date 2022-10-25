from rest_framework.permissions import BasePermission

from organizations.models import Organization

class IsOrganizationAdmin(BasePermission):
  def has_object_permission(self, request, view, obj):
    print('obj.organization', obj.organization)
    return obj.organization == request.user.organization

class IsSuperUser(BasePermission):
  def has_object_permission(self, request, view, obj):
    return request.user.is_superuser