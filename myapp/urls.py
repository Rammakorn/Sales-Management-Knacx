from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view()),
    path('create/', create_product, name='create-product'),
    path('read/', view_product, name='read-all-product'),
    path('read/<int:pk>/', view_specify_product, name='read-specify-product'),
    path('update/<int:pk>/', update_product, name='update-product'),
    path('delete/<int:pk>/', delete_product, name='delete-product'),
]