from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.encoding import force_bytes, force_str
from .forms import NewUserCreationFormCustomer, CompanyCreationForm, InvitationFormColleagues
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from user.models import NewUser, Employee, Customer
from django.contrib import messages
from .models import Company


# Create your views here.
def user_customer_check(user):
    return user.user_type == 2
# usage ---> @user_passes_test(user_customer_check, login_url='/')


def validate_colleagues_email(user, colleagues_email):
    # initializing strings
    test_str = colleagues_email
    # slicing domain name
    cleaned_domain = str(test_str.split('@')[1])
    return user.email.endswith(cleaned_domain)


def customerRegister(request, uu_id, customer_email):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
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
    form = NewUserCreationFormCustomer()
    company_form = CompanyCreationForm()
    context = {
        "form": form,
        "company_form": company_form,
        'clean_customer_email': clean_customer_email,
        'clean_uu_id': clean_uu_id,
        'related_employee': related_employee
    }
    if request.method == "POST":
        form = NewUserCreationFormCustomer(request.POST)
        company_form = CompanyCreationForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('company'):
                if company_form.is_valid():
                    if Company.objects.filter(name=company_form.cleaned_data.get('name').upper()):
                        messages.info(request, "This company already exist in company list.")
                    companyObj = company_form.save(commit=False)
                    companyObj.name = company_form.cleaned_data.get('name').upper()
                else:
                    messages.error(request, list(company_form.errors.values()) + [1])
                    return render(request, 'registerCustomer.html',
                                  context={'form': form, 'company_form': company_form})
            if form.cleaned_data.get('email') == clean_customer_email:
                customerObj = form.save(commit=False)
                customerObj.related_employee = related_employee
                customerObj.user_type = 2
                if not form.cleaned_data.get('company'):
                    companyObj.save()
                    customerObj.company = companyObj
                customerObj.save()
                messages.success(request, "Registration completed successfully.")
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.error(request, "This registration link is only valid for the emailed user.")
                return render(request, 'registerCustomer.html', context={'form': form, 'company_form': company_form})
        else:
            messages.error(request, list(form.errors.values()) + [1])
            return render(request, 'registerCustomer.html', context={'form': form, 'company_form': company_form})
    return render(request, "registerCustomer.html", context)


@login_required(login_url='/')
@user_passes_test(user_customer_check, login_url='/')
def dashboardCustomer(request):
    form = InvitationFormColleagues()
    colleagues = Customer.objects.filter(company__exact=request.user.customer.company).exclude(
        id=request.user.customer.id).order_by('-id')
    context = {
        "form": form,
        "colleagues": colleagues
    }
    if request.method == "POST":
        form = InvitationFormColleagues(request.POST)
        if form.is_valid():
            current_site = get_current_site(request)
            colleagues_email = form.cleaned_data.get('colleagues_email')
            if Customer.objects.filter(email=colleagues_email):
                messages.error(request, 'This user already exist')
                return render(request, "dashboardCustomer.html", context)
            if validate_colleagues_email(request.user, colleagues_email):
                mail_subject = 'XYZ Company customer registration link for colleagues.'
                employee_uuid = urlsafe_base64_encode(force_bytes(request.user.customer.related_employee.uu_id))
                customer_email_hash = urlsafe_base64_encode(force_bytes(colleagues_email))
                message = get_template('invitation_email.html').render({
                    'user': request.user,
                    'customer_email': colleagues_email,
                    'domain': current_site.domain,
                    'uid': employee_uuid,
                    'customer_email_hash': customer_email_hash
                })
                email = EmailMessage(
                    mail_subject, message, to=[colleagues_email]
                )
                email.content_subtype = "html"
                email.send()
                messages.success(request, 'Invitation link sent to colleague email address.')
                return HttpResponseRedirect(reverse("dashboardCustomer"))
            else:
                messages.info(request, 'Email recipient must have the same domain as you.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, "dashboardCustomer.html", context)
