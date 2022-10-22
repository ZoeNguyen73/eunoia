import uuid

from django.db import models
from django.utils import timezone

from .utils import OrganizationTypes, OrganizationStatuses
from eunoia.settings import PLACEHOLDER_LOGO

# Create your models here.
class Organization(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=200, blank=False, unique=True)
  description = models.CharField(max_length=200, blank=True)
  website = models.CharField(max_length=100, blank=True)
  email = models.EmailField(max_length=254, blank=True, unique=True)
  organization_type = models.CharField(
    max_length=254,
    choices=OrganizationTypes.choices(), 
    default=OrganizationTypes.DONOR, 
    blank=False,
    verbose_name="organization type",
  )
  status = models.CharField(
    max_length=254,
    choices=OrganizationStatuses.choices(),
    default=OrganizationStatuses.PENDING, 
    blank=False,
    verbose_name="organization status",
  )
  logo_url = models.URLField(max_length=254, default=PLACEHOLDER_LOGO)
  date_created = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.name
