from django.urls import path
from . import views

urlpatterns = [
     path('register/<uu_id>', views.customerRegister, name='customer_register'),
]