from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login as a_login
from django.contrib import messages
from .forms import LoginForm, NewUserCreationFormEmployee
from django.contrib.auth.decorators import login_required


# Create your views here.

def login(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return HttpResponseRedirect(reverse("dashboardEmployee"))
        elif request.user.user_type == 2:
            return HttpResponseRedirect(reverse("dashboardCustomer"))
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
                email=email,
                password=password,
            )
            if user is not None:
                a_login(request, user)
                messages.success(request, "Successfully logged in")
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    if user.user_type == 1:
                        return redirect("dashboardEmployee")
                    elif request.user.user_type == 2:
                        return redirect("dashboardCustomer")
            else:
                messages.error(request, "Invalid user")
    return render(request, "login.html", context)


@login_required(login_url='/')
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def registerEmployee(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    form = NewUserCreationFormEmployee()
    context = {
        'form': form,
    }
    if request.method == "POST":
        form = NewUserCreationFormEmployee(request.POST)
        if form.is_valid():
            employeeUserObj = form.save(commit=False)
            employeeUserObj.user_type = 1
            form.save()
            return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, list(form.errors.values()) + [1])
            return render(request, 'registerEmployee.html', context={'form': form})
    return render(request, 'registerEmployee.html', context)
