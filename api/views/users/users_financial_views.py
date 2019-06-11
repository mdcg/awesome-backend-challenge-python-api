from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum
from api.serializers.order_serializers import OrderSerializer


class UserFinancialReportView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        """
        A simple financial report.
        """
        user = request.user

        financial = user.orders.values('purchase_channel').annotate(
            count=Count('purchase_channel'), sum=Sum('total_value')
        )

        response_data = {
            'status': 'success',
            'data': {
                'financial': financial,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)
