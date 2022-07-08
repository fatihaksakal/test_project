from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from user.models import *
from user.forms import MyPasswordChangeForm, userProfileForm
from django.core.mail import send_mail
from django_cryptography.fields import b64encode, b64decode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.signing import Signer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.contrib import messages
from .forms import InvitationForm, EmployeeTaskFormCompany, EmployeeTaskFormCustomer
from .models import FutureCallLogs


# Create your views here.

def email_check_employee(user):
    return user.email.endswith('@xyz.com')


@login_required(login_url='/')
@user_passes_test(email_check_employee, login_url='/')
def dashboardEmployee(request):
    form = InvitationForm()
    related_customers = Customer.objects.filter(related_employee=request.user.employee)
    context = {
        "form": form,
        "related_customers": related_customers
    }
    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            # sending email to customer
            current_site = get_current_site(request)
            customer_email = form.cleaned_data.get("customer_email")
            if Customer.objects.filter(email=customer_email):
                messages.error(request, 'This user already exist')
                return render(request, "dashboardEmployee.html", context)
            mail_subject = 'XYZ Company customer registration link.'
            employee_uuid = urlsafe_base64_encode(force_bytes(request.user.employee.uu_id))
            customer_email_hash = urlsafe_base64_encode(force_bytes(customer_email))
            message = get_template('invitation_email.html').render({
                'user': request.user,
                'customer_email': customer_email,
                'domain': current_site.domain,
                'uid': employee_uuid,
                'customer_email_hash': customer_email_hash
            })
            email = EmailMessage(
                mail_subject, message, to=[customer_email]
            )
            email.content_subtype = "html"
            email.send()
            messages.success(request, "Invitation link sent to customer email address.")
            return HttpResponseRedirect(reverse("dashboardEmployee"))
        else:
            messages.error(request, list(form.errors.values()) + [1])
            return render(request, 'dashboardEmployee.html', context={'form': form})
    return render(request, "dashboardEmployee.html", context)


@login_required(login_url='/')
@user_passes_test(email_check_employee, login_url='/')
def employeeTask(request):
    form = EmployeeTaskFormCompany(request.user.employee)
    logs = FutureCallLogs.objects.filter(registrant=request.user.employee).order_by('-created_date')
    context = {
        "form": form,
        "logs": logs
    }
    if request.method == "POST":
        form = EmployeeTaskFormCompany(request.user.employee, request.POST)
        if form.is_valid():
            company = form.cleaned_data.get('company')
            customer_form = EmployeeTaskFormCustomer(request.user.employee, company.id)
            context['form'] = EmployeeTaskFormCompany(request.user.employee, initial={'company': company})
            context['customer_form'] = customer_form
            customer_form = EmployeeTaskFormCustomer(request.user.employee, company.id, request.POST)
            if customer_form.is_valid():
                customer = customer_form.cleaned_data.get('customer')
                content = customer_form.cleaned_data.get('content')
                if customer.company == company:
                    futureCallLog = FutureCallLogs(registrant=request.user.employee, company=company, customer=customer,
                                                   content=content)
                    futureCallLog.save()
                else:
                    messages.info(request, 'Customer and Company values does not match.')
                return HttpResponseRedirect(reverse("employeeTask"))
    return render(request, "employeeTask.html", context)


@login_required(login_url='/')
@user_passes_test(email_check_employee, login_url='/')
def customerOverview(request, pk):
    try:
        customer = Customer.objects.filter(id=force_str(urlsafe_base64_decode(pk)),
                                           related_employee=request.user.employee).first()
        logs = FutureCallLogs.objects.filter(customer=customer, registrant=request.user.employee)
    except(TypeError, ValueError, OverflowError):
        customer = None
        logs = None
    if not customer:
        return HttpResponseRedirect(reverse("dashboardEmployee"))
    context = {
        "customer": customer,
        "logs": logs
    }
    return render(request, "customerOverview.html", context)
