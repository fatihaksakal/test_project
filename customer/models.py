from django.db import models


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
