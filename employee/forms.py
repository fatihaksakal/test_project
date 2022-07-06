from django import forms


# Create your forms here.

class InvitationForm(forms.Form):
    customer_email = forms.EmailField(label="customer_email", max_length=200, widget=forms.EmailInput(
        attrs={'class': "form-control", 'id': 'customer_email_input', 'type': 'email', 'placeholder': 'Email Address',
               'aria-describedby': "emailHelp"}))
