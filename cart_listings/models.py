import uuid

from django.db import models
from carts.models import Cart
from listings.models import Listing

class Cart_Listing(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='cart_listing', null=True)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_listing', null=True)

  def __str__(self):
    return self.id