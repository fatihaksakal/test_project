from django import forms
from customer.models import Company
from user.models import Customer, Employee


# Create your forms here.

class InvitationForm(forms.Form):
    customer_email = forms.EmailField(label="customer_email", max_length=200, widget=forms.EmailInput(
        attrs={'class': "form-control", 'id': 'customer_email_input', 'type': 'email', 'placeholder': 'Email Address',
               'aria-describedby': "emailHelp"}))


class EmployeeTaskFormCompany(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EmployeeTaskFormCompany, self).__init__(*args, **kwargs)
        self.fields['company'] = forms.ChoiceField(
            choices=[(company.id, str(company)) for company in Company.objects.filter(
                id__in=Customer.objects.filter(related_employee=user).values_list('company').distinct())]
        )
        self.fields['company'].widget.attrs['class'] = 'form-control'


class EmployeeTaskFormCustomer(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, company_value, *args, **kwargs):
        super(EmployeeTaskFormCustomer, self).__init__(*args, **kwargs)
        self.fields['customer'] = forms.ChoiceField(
            choices=[(customer.id, str(customer)) for customer in Customer.objects.filter(
                related_employee=user, company=company_value)]
        )
        self.fields['customer'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['class'] = 'form-control'
