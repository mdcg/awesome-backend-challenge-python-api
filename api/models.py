from django.contrib.auth.models import User
from django.db import models
from api.constants import STATUS, READY


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(BaseModel):
    reference = models.CharField(max_length=100)
    purchase_channel = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    delivery_service = models.CharField(max_length=100)
    total_value = models.DecimalField(max_digits=6, decimal_places=2)
    line_items = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=STATUS, default=READY)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='orders')

    def __str__(self):
        return f'{self.id} - {self.reference} - ({self.created_at})'


class Batch(BaseModel):
    reference = models.CharField(max_length=100)
    purchase_channel = models.CharField(max_length=100)
    orders = models.ManyToManyField(Order, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='batches')

    def __str__(self):
        return f'{self.id} - {self.reference} - ({self.created_at})'
