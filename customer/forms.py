from django import forms
from user.models import Customer
from .models import Company
from user.forms import NewUserCreationForm


class NewUserCreationFormCustomer(NewUserCreationForm):
    class Meta:
        model = Customer
        fields = ('company', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(NewUserCreationFormCustomer, self).__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'form-control'


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class InvitationFormColleagues(forms.Form):
    colleagues_email = forms.EmailField(label="colleagues_email", max_length=200, widget=forms.EmailInput(
        attrs={'class': "form-control", 'id': 'customer_email_input', 'type': 'email', 'placeholder': 'Email Address',
               'aria-describedby': "emailHelp"}))
