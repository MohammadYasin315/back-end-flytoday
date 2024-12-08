from rest_framework import serializers, status
from decimal import Decimal
from .models import Reservation, PaymentInfo
from django.core.exceptions import ValidationError 

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'room', 'check_in', 'check_out', 'adults',
            'total_price', 'created_at', 'updated_at', 'first_name',
            'last_name', 'nationality', 'passport_number', 'gender',
        ]   
    
    def validate(self, data):
        """اجرای اعتبارسنجی مدل"""
        instance = Reservation(**data)  
        try:
            instance.clean()  
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)  
        return data


class PaymentInfoSerializer(serializers.ModelSerializer):
    tracking_code = serializers.ReadOnlyField()
    discounted_price = serializers.SerializerMethodField()
    reservation_details = ReservationSerializer(source='reservation', read_only=True)

    class Meta:
        model = PaymentInfo
        fields = [
            'id', 'reservation', 'reservation_details', 'discount_code',
            'description', 'accepted_terms', 'tracking_code', 'discounted_price',
        ]


    def validate(self, data):
        """اجرای اعتبارسنجی مدل"""
        instance = PaymentInfo(**data)  
        try:
            instance.clean()  
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return data
    

    def get_discounted_price(self, obj):
        """دریافت قیمت تخفیف‌خورده از متد مدل"""
        return obj.get_discounted_price()
    

    def validate_discount_code(self, value):
        """اعتبارسنجی کد تخفیف"""
        if value and value != "OFF100":
            raise serializers.ValidationError("کد تخفیف نامعتبر است.")
        return value
