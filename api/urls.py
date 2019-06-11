from django.contrib import admin
from django.urls import path

from api.views.orders.orders_details_views import (OrderDetailsView,
                                                   OrdersSearchView)
from api.views.orders.orders_views import OrdersView
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
    #
    # Orders
    #
    path(
        'orders',
        OrdersView.as_view(),
        name='orders',
    ),
    path(
        'orders/search',
        OrdersSearchView.as_view(),
        name='orders_search',
    ),
    path(
        'orders/<int:order_id>',
        OrderDetailsView.as_view(),
        name='order_details',
    ),

]
