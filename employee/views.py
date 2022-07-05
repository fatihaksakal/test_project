from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from user.models import *
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.signing import Signer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import InvitationForm


# Create your views here.

def email_check_employee(user):
    return user.email.endswith('@xyz.com')


@login_required(login_url='/')
@user_passes_test(email_check_employee, login_url='/')
def dashboardEmployee(request):
    form = InvitationForm()
    context = {
        "form": form
    }
    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            # sending email to customer
            current_site = get_current_site(request)
            customer_email = form.cleaned_data.get("customer_email")
            mail_subject = 'This account is awaiting your approval.'
            signer = Signer()
            value = signer.sign(request.user.employee.uu_id)
            message = render_to_string('invitation_email.html', {
                'user': request.user,
                'customer_email': customer_email,
                'domain': current_site.domain,
                'uid': value
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
