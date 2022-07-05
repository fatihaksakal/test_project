from django import forms
from .models import NewUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


# Create your forms here.

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=200, widget=forms.EmailInput(
        attrs={'class': "form-control", 'id': 'floatingEmail', 'placeholder': 'Email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': 'floatingPassword', 'placeholder': 'Password'}))


class NewUserCreationFormEmployee(UserCreationForm):
    email = forms.EmailField(required=True, label="Email", max_length=200, widget=forms.EmailInput(
        attrs={'class': "form-control", 'id': 'floatingEmail', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(
        attrs={'class': "form-control", 'id': 'floatingFirstName', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(
        attrs={'class': "form-control", 'id': 'floatingLastName', 'placeholder': 'Last Name'}))

    def clean(self):
        email = self.cleaned_data.get("email")
        if not email.endswith('@xyz.com'):
            raise ValidationError("This registration just for xyz.com mail users.")
        else:
            return email

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirmation'

    class Meta(UserCreationForm):
        model = NewUser
        fields = ('email', 'first_name', 'last_name')
