from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from user.models import *
from django.core.mail import send_mail
from django_cryptography.fields import b64encode, b64decode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.core.signing import Signer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import InvitationForm
from user.models import Customer


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
            mail_subject = 'This account is awaiting your approval.'
            employee_uuid = urlsafe_base64_encode(force_bytes(request.user.employee.uu_id))
            customer_email_hash = urlsafe_base64_encode(force_bytes(customer_email))
            message = render_to_string('invitation_email.html', {
                'user': request.user,
                'customer_email': customer_email,
                'domain': current_site.domain,
                'uid': employee_uuid,
                'customer_email_hash': customer_email_hash
            })
            email = EmailMessage(
                mail_subject, message, to=[customer_email]
            )
            email.send()
            messages.success(request, "Invitation link send to customer email address.")
            return HttpResponseRedirect(reverse("dashboardEmployee"))
        else:
            messages.error(request, list(form.errors.values()) + [1])
            return render(request, 'dashboardEmployee.html', context={'form': form})
    return render(request, "dashboardEmployee.html", context)
