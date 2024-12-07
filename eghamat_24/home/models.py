from django.db import models
from iranian_cities.fields import ProvinceField

# City models
class City(models.Model):
    city = ProvinceField()

    def __str__(self):
        return str(self.city)
