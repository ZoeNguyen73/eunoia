import uuid

from django.db import models
from organizations.models import Organization

class Cart(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='cart')

  def __str__(self):
    return self.id
