from user.models import Customer
from user.forms import NewUserCreationForm


class NewUserCreationFormCustomer(NewUserCreationForm):
    class Meta:
        model = Customer
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
