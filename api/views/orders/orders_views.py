from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.order_serializers import OrderSerializer


class OrdersView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        """
        Create a new Order.
        """
        user = request.user
        order_data = OrderSerializer(data=request.data)

        if order_data.is_valid():
            order = order_data.save(user=user)
            serialized_order = OrderSerializer(order)

            response_data = {
                'status': 'success',
                'data': {
                    'order': serialized_order.data,
                },
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        response_data = {
            'status': 'fail',
            'data': order_data.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        """
        List the Orders of a Purchase Channel.
        """
        user = request.user

        purchase_channel = request.query_params.get('purchase_channel', None)

        if purchase_channel:
            orders = user.orders.filter(
                status='ready', purchase_channel=purchase_channel)
        else:
            orders = user.orders.filter(
                status='ready')

        serialized_orders = OrderSerializer(
            orders, many=True)

        response_data = {
            'status': 'success',
            'data': {
                'orders': serialized_orders.data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)
