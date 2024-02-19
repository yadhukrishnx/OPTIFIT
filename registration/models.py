from django.db import models
from django.contrib.auth.models import User

class ProfileData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)  
