import uuid

from django.db import models
from django.core.validators import RegexValidator

from organizations.models import Organization

class Address(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=50, blank=False)
  contact_name = models.CharField(max_length=50, blank=False)
  contact_number = models.CharField(max_length=50, blank=False)
  details = models.CharField(max_length=200, blank=False)
  postal_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{1,10}$')])
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='addresses')
  is_default = models.BooleanField(default=False)

  def __str__(self):
    return self.name