from django import forms


# Create your forms here.

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=200, widget=forms.EmailInput(
        attrs={'class': "form-control", 'id': 'floatingEmail', 'placeholder': 'Email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': 'floatingPassword', 'placeholder': 'Password'}))
