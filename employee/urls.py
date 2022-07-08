from django.urls import path
from . import views
from user.views import profile

urlpatterns = [
    path('', views.dashboardEmployee, name='dashboardEmployee'),
    path('duties/', views.employeeTask, name='employeeTask'),
    path('profile/', profile, name='employeeProfile'),
    path('detail/customer/<slug:pk>', views.customerOverview, name='customerOverview'),
]
