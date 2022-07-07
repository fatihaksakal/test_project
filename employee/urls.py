from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardEmployee, name='dashboardEmployee'),
    path('task/', views.employeeTask, name='employeeTask'),
]
