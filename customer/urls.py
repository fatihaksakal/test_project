from django.urls import path
from . import views

urlpatterns = [
     path('', views.dashboardCustomer, name='dashboardCustomer'),
     path('register/<uu_id>/<customer_email>', views.customerRegister, name='customer_register'),
]