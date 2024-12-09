from django.db import models
from django.contrib.auth.models import AbstractUser

# User models
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return str(self.phone_number)


# UserProfile models
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, blank=True) 
    last_name = models.CharField(max_length=50, null=True, blank=True)   
    national_code = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    landline = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return str(self.user)
