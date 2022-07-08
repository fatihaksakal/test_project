from django.urls import path
from . import views
from user.views import profile

urlpatterns = [
    path('', views.dashboardCustomer, name='dashboardCustomer'),
    path('register/<uu_id>/<customer_email>', views.customerRegister, name='customer_register'),
    path('profile/', profile, name='customerProfile'),
]
