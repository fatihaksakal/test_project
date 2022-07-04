from django.urls import path
from . import views

urlpatterns = [
     path('', views.login, name='login'),
     path('logout/', views.logoutUser, name="logout"),
     path('register/employee/', views.registerEmployee, name="registerEmployee"),
]
