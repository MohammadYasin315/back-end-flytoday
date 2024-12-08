from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile
from reservations.models import Reservation, PaymentInfo

# Serializer for registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password', 'email']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user


# Serializer for login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, value):
        username = value.get('username')
        password = value.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("نام کاربری یا رمز عبور نامعتبر است")

        value['user'] = user
        return value
    

# Serializer for list, retrieve, update
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'national_code', 'birth_date', 'address', 'landline']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'national_code', 'birth_date', 'address', 'landline']



# Serializer for Reservation
class UserReservationSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()  
    tracking_code = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id', 'room', 'check_in', 'check_out', 'adults', 'total_price',
            'discounted_price', 'payment_status', 'tracking_code',
        ]

    def get_discounted_price(self, obj):
        """دریافت قیمت تخفیف‌خورده از PaymentInfo"""
        payment_info = PaymentInfo.objects.filter(reservation=obj).first()
        if payment_info:
            return payment_info.get_discounted_price()
        return None
    
    
    def get_payment_status(self, obj):
        """دریافت وضعیت پرداخت"""
        return obj.get_payment_status()


    def get_tracking_code(self, obj):
        """کد پیگیری از PaymentInfo"""
        payment_info = PaymentInfo.objects.filter(reservation=obj).first()
        if payment_info:
            return payment_info.tracking_code
        return None
    