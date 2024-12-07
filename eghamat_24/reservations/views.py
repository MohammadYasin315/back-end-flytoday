from rest_framework import viewsets, permissions, serializers
from rest_framework.response import Response
from .models import Reservation, PaymentInfo
from .serializers import ReservationSerializer, PaymentInfoSerializer
from accounts.models import UserProfile

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        """نمایش فقط رزروهای کاربر جاری"""
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ایجاد رزرو برای کاربر جاری"""
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user=user_profile)


class PaymentInfoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentInfoSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        """نمایش فقط اطلاعات پرداخت کاربر جاری"""
        return PaymentInfo.objects.filter(reservation__user=self.request.user)

    def perform_create(self, serializer):
        """ایجاد پرداخت برای رزرو کاربر"""
        reservation = serializer.validated_data.get('reservation')
        if reservation.user.user != self.request.user:
            raise serializers.ValidationError("شما نمی‌توانید برای رزروهای دیگران پرداخت ایجاد کنید.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        """افزودن پیام موفقیت‌آمیز به پاسخ"""
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "تراکنش موفقیت‌آمیز بود."
        return response
