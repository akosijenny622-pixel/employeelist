from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    phone = models.CharField(max_length=15, blank=True)

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff

    def get_role_display(self):
        """
        Override the default get_role_display to check superuser/staff status.
        This ensures admins are always displayed correctly even if role field wasn't set.
        """
        if self.is_superuser or self.is_staff or self.role == 'admin':
            return 'Admin'
        # Otherwise use the role field
        return dict(self.ROLE_CHOICES).get(self.role, 'Employee')

class Employee(models.Model):
    DEPARTMENT_CHOICES = (
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('FIN', 'Finance'),
        ('MKT', 'Marketing'),
        ('OPS', 'Operations'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"

    class Meta:
        ordering = ['-created_at']

# Create your models here.
