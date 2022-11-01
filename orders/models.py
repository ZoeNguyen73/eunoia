from re import T
import uuid

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

from timeslots.utils import TimeslotOptions
from .utils import OrderStatuses

class Order(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  date_created = models.DateTimeField(default=timezone.now)
  donor_org_name = models.CharField(max_length=200, blank=False)
  donor_org_id = models.CharField(max_length=200, blank=False)
  charity_org_name = models.CharField(max_length=200, blank=False)
  charity_org_id = models.CharField(max_length=200, blank=False)
  collection_date = models.DateField()
  collection_timeslot = models.CharField(
    max_length=254,
    choices=TimeslotOptions.choices(), 
    blank=False,
    verbose_name='timeslot option',
  )
  collection_address_contact_name = models.CharField(max_length=50, blank=False)
  collection_address_contact_number = models.CharField(max_length=50, blank=False)
  collection_address_details = models.CharField(max_length=200, blank=False)
  collection_address_postal_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{1,10}$')])
  delivery_address_contact_name = models.CharField(max_length=50, blank=False)
  delivery_address_contact_number = models.CharField(max_length=50, blank=False)
  delivery_address_details = models.CharField(max_length=200, blank=False)
  delivery_address_postal_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{1,10}$')])
  completion_time = models.DateTimeField(null=True)
  need_delivery = models.BooleanField(default=False)
  status = models.CharField(
    max_length=254,
    choices=OrderStatuses.choices(), 
    default='open',
    blank=False,
    verbose_name='order status',
  )

  class Meta:
    ordering = ['-date_created']

  def __str__(self):
    return self.id

