from tkinter import CASCADE
import uuid

from django.db import models
from django.utils import timezone

from organizations.models import Organization
from .utils import ItemTypes

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
  organization = models.ForeignKey(Organization, on_delete=CASCADE, related_name='items')
  date_created = models.DateTimeField(default=timezone.now)
  
  class Meta:
    ordering = ['-date_created']
  
  def __str__(self):
    return self.name