from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class UsersAdmin(UserAdmin):
  list_display = ('email', 'username', 'date_joined', 'is_admin', 'is_superuser')
  search_fields = ('email', 'username')
  readonly_fields = ('id', 'date_joined')
  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()

admin.site.register(User, UsersAdmin)