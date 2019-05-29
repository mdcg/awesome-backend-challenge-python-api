from django.contrib.auth.models import User
from api.models import Order, Batch


def create_user(**kwargs):
    return User.objects.create(**kwargs)

def create_order(**kwargs):
    return Order.objects.create(**kwargs)

def create_batch(**kwargs):
    return Batch.objects.create(**kwargs)