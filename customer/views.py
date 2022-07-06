from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import NewUserCreationFormCustomer
from user.models import NewUser, Employee, Customer
from django.contrib import messages


# Create your views here.

def customerRegister(request, uu_id, customer_email):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return HttpResponseRedirect(reverse("dashboardEmployee"))
    form = NewUserCreationFormCustomer()
    context = {
        "form": form
    }
    try:
        clean_customer_email = force_str(urlsafe_base64_decode(customer_email))
        clean_uu_id = force_str(urlsafe_base64_decode(uu_id))
        related_employee = Employee.objects.filter(uu_id=clean_uu_id).first()
    except(TypeError, ValueError, OverflowError, NewUser.DoesNotExist):
        clean_customer_email = None
        clean_uu_id = None
        related_employee = None
    if Customer.objects.filter(email=clean_customer_email):
        messages.error(request, "This registration link already used. Please authenticate yourself.")
        return HttpResponseRedirect(reverse("login"))
    context['clean_customer_email'] = clean_customer_email
    context['clean_uu_id'] = clean_uu_id
    context['related_employee'] = related_employee
    if request.method == "POST":
        form = NewUserCreationFormCustomer(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('email') == clean_customer_email:
                customerObj = form.save(commit=False)
                customerObj.related_employee = related_employee
                customerObj.user_type = 2
                customerObj.save()
                messages.success(request, "Registration completed successfully.")
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.error(request, "This registration link is only valid for the emailed user.")
                return render(request, 'registerCustomer.html', context={'form': form})
        else:
            messages.error(request, list(form.errors.values()) + [1])
            return render(request, 'registerCustomer.html', context={'form': form})
    return render(request, "registerCustomer.html", context)


def dashboardCustomer(request):
    return render(request, "dashboardCustomer.html")
