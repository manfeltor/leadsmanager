from django.contrib.auth.models import AbstractUser
from django.db import models

MANAGEMENT_ROLES = {'admin', 'manager'}
EMPLOYEE_ROLES = {'employee'}

class CustomUser(AbstractUser):
    MANAGER = 'manager'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
        (ADMIN, 'Admin'),
    ]

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE)
    mail = models.EmailField(blank=False, null=False, )

    def __str__(self):
        return self.username

class UserAttribute(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attributes')
    value1 = models.CharField(max_length=50, blank=True, null=True)
    value2 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'