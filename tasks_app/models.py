from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    SUPERADMIN = 'SUPERADMIN'
    ADMIN = 'ADMIN'
    USER = 'USER'
    ROLE_CHOICES = [
    (SUPERADMIN, 'SuperAdmin'),
    (ADMIN, 'Admin'),
    (USER, 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)


    def is_superadmin(self):
        return self.role == self.SUPERADMIN


    def is_admin(self):
        return self.role == self.ADMIN




class Task(models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (IN_PROGRESS, 'In Progress'),
    (COMPLETED, 'Completed'),
    ]


    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)


    completion_report = models.TextField(null=True, blank=True)
    worked_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} ({self.status})"