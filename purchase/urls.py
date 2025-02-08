from django.urls import path
from .views import *


urlpatterns = [
    # path('', test),
    path('create/', create_order, name='create-order'),
    path('', get_orders, name='read-order'),
    path('confirm/<int:pk>/', confirm_order, name='confirm-order'),
]