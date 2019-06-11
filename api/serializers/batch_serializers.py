from rest_framework import serializers

from api.models import Batch
from api.serializers.order_serializers import OrderSerializer


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        exclude = ('user',)


class BatchDetailsSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Batch
        exclude = ('user',)
