from django.db import models
from user.models import Employee, Customer
from customer.models import Company


# Create your models here.

class FutureCallLogs(models.Model):
    registrant = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()
