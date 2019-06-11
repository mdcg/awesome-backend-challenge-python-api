from django.contrib import admin
from django.urls import path

from api.views.batches.batches_views import (BatchCloseToDeliveryServiceView,
                                             BatchProduceView, BatchView)
from api.views.orders.orders_details_views import (OrderDetailsView,
                                                   OrdersSearchView)
from api.views.orders.orders_views import OrdersView
from api.views.users.users_financial_views import UserFinancialReportView
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
    path(
        'users/financial-report',
        UserFinancialReportView.as_view(),
        name='user_financial_report',
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
    #
    # Batches
    #
    path(
        'batches',
        BatchView.as_view(),
        name='batches',
    ),
    path(
        'batches/<int:batch_id>/produce',
        BatchProduceView.as_view(),
        name='produce-batch',
    ),
    path(
        'batches/<int:batch_id>/send',
        BatchCloseToDeliveryServiceView.as_view(),
        name='send-batch',
    ),
]
