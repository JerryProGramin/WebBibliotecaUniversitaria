# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class StaffRole(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.ForeignKey(StaffRole, on_delete=models.SET_NULL, null=True, blank=True)
    is_active_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
