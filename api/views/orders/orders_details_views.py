from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Order
from api.serializers.order_serializers import OrderSerializer


class OrderDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, order_id, format=None):
        """
        Details of an order.
        """
        user = request.user

        try:
            order = Order.objects.get(
                id=order_id,
                user=user,
            )
        except ObjectDoesNotExist:
            response_data = {
                'status': 'fail',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serialized_order = OrderSerializer(order)

        response_data = {
            'status': 'success',
            'data': {
                'order': serialized_order.data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)


class OrdersSearchView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        """
        Search orders
        """
        user = request.user

        reference = request.query_params.get('reference', None)

        if reference:
            orders = user.orders.filter(reference=reference)
        else:
            orders = user.orders.all()

        serialized_orders = OrderSerializer(orders, many=True)

        response_data = {
            'status': 'success',
            'data': {
                'orders': serialized_orders.data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)
