from django.db import models
from django.contrib.auth.models import AbstractUser

# UserProfile model
class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)  
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)  
    national_code = models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)  
    address = models.TextField(max_length=200, null=True, blank=True)  
    landline = models.CharField(max_length=11, null=True, blank=True)  

    def __str__(self):
        return f"{self.username} ({self.phone_number})"
