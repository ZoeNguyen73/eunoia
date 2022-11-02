import uuid

from django.db import models

from listings.models import Listing
from .utils import TimeslotOptions

class Timeslot(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  date = models.DateField()
  timeslot_option = models.CharField(
    max_length=254,
    choices=TimeslotOptions.choices(), 
    blank=False,
    verbose_name='timeslot option',
  )
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')

  def __str__(self):
    return self.id
