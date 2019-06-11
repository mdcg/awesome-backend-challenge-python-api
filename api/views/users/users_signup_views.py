from django.contrib.auth.models import User
from rest_framework import authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user_serializers import UserSerializer


class UserSignUpView(APIView):

    def post(self, request, format=None):
        user_registration_data = UserSerializer(
            data=request.data)

        if user_registration_data.is_valid():
            user = user_registration_data.save()
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
            return Response(response_data, status=status.HTTP_201_CREATED)

        response_data = {
            'status': 'fail',
            'data': user_registration_data.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
