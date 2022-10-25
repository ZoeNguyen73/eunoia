import uuid

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

from .utils import OrganizationTypes, OrganizationStatuses, unique_slug_generator
from eunoia.settings import PLACEHOLDER_LOGO

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
    default='pending', 
    blank=False,
    verbose_name="organization status",
  )
  logo_url = models.URLField(max_length=254, default=PLACEHOLDER_LOGO)
  logo_id = models.CharField(max_length=150, blank=True)
  slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
  date_created = models.DateTimeField(default=timezone.now)

  class Meta:
    ordering = ['-date_created']

  def __str__(self):
    return self.name

@receiver(pre_save, sender=Organization)
def pre_save_receiver(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)