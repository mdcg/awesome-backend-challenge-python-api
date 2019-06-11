from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.constants import CLOSING, PRODUCTION, READY, SENT
from api.models import Batch
from api.serializers.batch_serializers import (BatchDetailsSerializer,
                                               BatchSerializer)


class BatchView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        """
        Create a Batch.
        """
        user = request.user

        batch_data = BatchSerializer(data=request.data)

        if batch_data.is_valid():

            orders = user.orders.filter(
                purchase_channel=request.data.get('purchase_channel'),
                status=READY,
            )

            if not orders:
                response_data = {
                    'status': 'fail',
                    'data': {
                        'purchase_channel': [
                            'There are no orders with this purchase channel to go to production.',
                        ],
                    },
                }
                return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            batch = batch_data.save(user=user)

            for order in orders:
                order.status = PRODUCTION
                order.save()
                batch.orders.add(order)

            batch.save()

            serialized_batch = BatchDetailsSerializer(batch)

            response_data = {
                'status': 'success',
                'data': {
                    'batch': serialized_batch.data,
                },
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        response_data = {
            'status': 'fail',
            'data': batch_data.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class BatchProduceView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, batch_id, format=None):
        """
        Produce a Batch.
        """
        user = request.user

        try:
            batch = Batch.objects.get(
                id=batch_id,
                user=user,
            )
        except ObjectDoesNotExist:
            response_data = {
                'status': 'fail',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        orders = batch.orders.filter(
            status=PRODUCTION,
        )

        if not orders:
            response_data = {
                'status': 'fail',
                'data': {
                    'purchase_channel': [
                        'There are no orders with this purchase channel to produce.',
                    ],
                },
            }
            return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        for order in orders:
            order.status = CLOSING
            order.save()

        serialized_batch = BatchDetailsSerializer(batch)

        response_data = {
            'status': 'success',
            'data': {
                'batch': serialized_batch.data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)


class BatchCloseToDeliveryServiceView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, batch_id, format=None):
        """
        Close part of a Batch for a Delivery Service.
        """
        user = request.user
        delivery_service = request.data.get('delivery_service', None)

        if not delivery_service:
            response_data = {
                'status': 'fail',
                'data': {
                    'delivery_service': ['This field is required.'],
                },
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            batch = Batch.objects.get(
                id=batch_id,
                user=user,
            )
        except ObjectDoesNotExist:
            response_data = {
                'status': 'fail',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        orders = batch.orders.filter(
            status=CLOSING,
            delivery_service=delivery_service
        )

        if not orders:
            response_data = {
                'status': 'fail',
                'data': {
                    'purchase_channel': [
                        'There are no orders with this delivery service to send.',
                    ],
                },
            }
            return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        for order in orders:
            order.status = SENT
            order.save()

        serialized_batch = BatchDetailsSerializer(batch)

        response_data = {
            'status': 'success',
            'data': {
                'batch': serialized_batch.data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)
