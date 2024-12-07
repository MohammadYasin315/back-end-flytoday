from rest_framework import serializers
from .models import City

class CitySerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'city_name']

    def get_city_name(self, obj):
        return str(obj.city)
