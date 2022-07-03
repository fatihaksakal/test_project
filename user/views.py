from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login as a_login
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
    }
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(
                request=request,  # for django_axes_logs
                email=email,
                password=password,
            )
        # messages.success(request, "Logged in successfully.")
    return render(request, "index.html", context)
