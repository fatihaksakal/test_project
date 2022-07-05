from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


# Create your views here.

def email_check_employee(user):
    return user.email.endswith('@xyz.com')


@login_required(login_url='/')
# @user_passes_test(email_check_employee, login_url='/')
def dashboardEmployee(request):
    return render(request, "dashboardEmployee.html")
