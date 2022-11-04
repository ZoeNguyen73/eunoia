import uuid

from django.db import models
from django.utils import timezone

from organizations.models import Organization
from items.models import Item
from addresses.models import Address
from .utils import ListingStatuses, TimeslotOptions

class Listing(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='listing', null=True)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='listing', null=True)
  collection_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='listing', null=True)
  amount = models.CharField(max_length=254, blank=False, verbose_name='amount')
  status = models.CharField(
    max_length=254,
    choices=ListingStatuses.choices(),
    default='inactive', 
    blank=False,
    verbose_name='listing status',
  )
  expiry_date = models.DateField(null=True, blank=True)
  collection_date = models.DateField(default=timezone.now)
  timeslot = models.CharField(
    max_length=254,
    choices=TimeslotOptions.choices(), 
    blank=False,
    verbose_name='timeslot option',
  )
  date_created = models.DateTimeField(default=timezone.now)

  class Meta:
    ordering = ['-date_created']
  
  def __str__(self):
    return self.id
