import uuid

from eunoia.settings import PLACEHOLDER_PROFILE_IMAGE
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db import models

from organizations.models import Organization
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  username = models.CharField(verbose_name='username', unique=True, max_length=30)
  email = models.EmailField(verbose_name="email", max_length=50, unique=True)
  profile_image = models.URLField(max_length=254, default=PLACEHOLDER_PROFILE_IMAGE)
  organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name='admins', null=True)
  contact_number = models.CharField(max_length=20)
  date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  objects = UserManager()

  def __str__(self):
    return self.username
  
