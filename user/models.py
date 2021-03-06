from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
from customer.models import Company
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class NewUser(AbstractUser):
    EMPLOYEE = 1
    CUSTOMER = 2
    user_type_choices = [
        (EMPLOYEE, 'Employee'),
        (CUSTOMER, 'Customer')
    ]
    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.PositiveSmallIntegerField(choices=user_type_choices, null=True, blank=True, default='')
    bio = models.TextField(max_length=300, default='')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Employee(NewUser):
    uu_id = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        verbose_name = 'Employee'


class Customer(NewUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='Not defined', null=True, blank=True)
    related_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Customer'

    def get_absolute_url(self):
        return reverse('customerOverview', kwargs={'pk': urlsafe_base64_encode(force_bytes(self.id))})
