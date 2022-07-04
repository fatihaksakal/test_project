from django import forms
from .models import NewUser
from django.contrib.auth.forms import UserCreationForm


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

    class Meta(UserCreationForm):
        model = NewUser
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirmation'