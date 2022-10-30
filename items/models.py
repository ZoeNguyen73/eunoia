import uuid

from django.db import models
from django.utils import timezone

from organizations.models import Organization
from .utils import ItemTypes
from eunoia.settings import PLACEHOLDER_LOGO

class Item(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100, blank=False)
  description = models.CharField(max_length=200, blank=True)
  item_type = models.CharField(
    max_length=254,
    choices=ItemTypes.choices(), 
    default='Miscellaneous', 
    blank=False,
    verbose_name='item type',
  )
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='items')
  image_url = models.URLField(max_length=254, default=PLACEHOLDER_LOGO)
  image_id = models.CharField(max_length=150, blank=True)
  date_created = models.DateTimeField(default=timezone.now)
  
  class Meta:
    ordering = ['-date_created']
  
  def __str__(self):
    return self.name