from django.contrib import admin
from django.urls import path

from api.views.users.users_signin_views import UserSignInView
from api.views.users.users_signup_views import UserSignUpView

urlpatterns = [
    #
    # Users
    #
    path(
        'users/signup',
        UserSignUpView.as_view(),
        name='user_signup',
    ),
    path(
        'users/signin',
        UserSignInView.as_view(),
        name='user_signin',
    ),
]
