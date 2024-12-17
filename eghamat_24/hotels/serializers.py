from rest_framework import serializers
from .models import Hotel, Room, Review


class HotelSummarySerializer(serializers.ModelSerializer):
    starting_price = serializers.IntegerField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'general_info', 'location', 'rating', 'starting_price']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'price_per_night', 'cancellation_policy', 'breakfast_included']


class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)  
    reviews = ReviewSerializer(many=True, read_only=True)  

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'general_info', 'hotel_info', 'location', 'facilities',
                  'restaurants_and_cafes', 'rules', 'rating', 'faqs', 'rooms', 'reviews']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'hotel', 'rating', 'comment', 'created_at']  
