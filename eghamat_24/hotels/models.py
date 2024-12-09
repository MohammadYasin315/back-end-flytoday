from django.db import models
from accounts.models import CustomUser
from django.core.validators import MaxValueValidator
from home.models import City

# Hotel models
class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=100)  
    general_info = models.TextField() 
    hotel_info = models.TextField()
    location = models.CharField(max_length=100)
    facilities = models.TextField(default=list) 
    restaurants_and_cafes = models.TextField(default=list)
    rules = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    faqs = models.TextField(default=list, blank=True) 

    def __str__(self):
        return self.name

# Room models
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')  
    name = models.CharField(max_length=255) 
    price_per_night = models.DecimalField(max_digits=20, decimal_places=0) 
    cancellation_policy = models.TextField(null=True, blank=True)  
    breakfast_included = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"

# Review models
class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)]) 
    comment = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name}"

