import uuid

from django.db import models
from orders.models import Order
from eunoia.settings import PLACEHOLDER_LOGO

class Order_Listing(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_listing', null=True)
  name = models.CharField(max_length=100, blank=False)
  description = models.CharField(max_length=200, blank=True)
  expiry_date = models.DateField(null=True, blank=True)
  image_url = models.URLField(max_length=254, default=PLACEHOLDER_LOGO)

  def __str__(self):
    return self.id