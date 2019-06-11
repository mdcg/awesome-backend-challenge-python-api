from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user_serializers import UserSerializer


class UserSignInView(APIView):

    def post(self, request, format=None):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username:
            response_data = {
                'status': 'fail',
                'data': {
                    'username': ['This field is required.'],
                },
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            response_data = {
                'status': 'fail',
                'data': {
                    'password': ['This field is required.'],
                },
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                'status': 'success',
                'data': {
                    'user': {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'token': token.key,
                    },
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            'status': 'fail',
            'data': {
                'username': ['Invalid username.'],
                'password': ['Invalid password.'],
            },
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
