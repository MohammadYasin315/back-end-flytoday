import random
import string
from django.db import models
from django.core.exceptions import ValidationError
from hotels.models import Room
from accounts.models import UserProfile

class Reservation(models.Model):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    
    STATUS_CHOICES = [
        (PENDING, 'در انتظار پرداخت'),
        (SUCCESS, 'موفق'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reservations", null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations", verbose_name="اتاق")
    check_in = models.DateField(verbose_name="تاریخ ورود")
    check_out = models.DateField(verbose_name="تاریخ خروج")
    adults = models.PositiveIntegerField(verbose_name="تعداد بزرگسالان")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name="قیمت کل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    GENDER_CHOICES = [
        ('M', 'مرد'),
        ('F', 'زن'),
    ]
    NATIONALITY_CHOICES = [
        ('IR', 'ایرانی'),
        ('NON_IR', 'غیر ایرانی'),
    ]
    first_name = models.CharField(max_length=100, verbose_name="نام", blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی", blank=True, null=True)
    nationality = models.CharField(max_length=10, choices=NATIONALITY_CHOICES, verbose_name="ملیت", blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره پاسپورت")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت رزرو")

    def get_payment_status(self):
        """بررسی وضعیت پرداخت"""
        payment_info = PaymentInfo.objects.filter(reservation=self).first()
        if payment_info and payment_info.tracking_code: 
            return 'موفق'
        return 'در انتظار پرداخت'


    def get_status_display_farsi(self):
        """بازگرداندن وضعیت به‌صورت فارسی"""
        status_dict = {
            'PENDING': 'در انتظار پرداخت',
            'SUCCESS': 'موفق',
            'FAILED': 'ناموفق',
        }
        return status_dict.get(self.status, 'نامشخص')

    def calculate_price(self):
        """محاسبه قیمت کل رزرو بر اساس تعداد شب‌ها"""
        nights = (self.check_out - self.check_in).days
        if nights <= 0:
            raise ValidationError("تاریخ خروج باید بعد از تاریخ ورود باشد.")
        self.total_price = nights * self.room.price_per_night

    def clean(self):
        """ولیدیشن برای جلوگیری از تداخل رزروها"""
        if self.check_in >= self.check_out:
            raise ValidationError("تاریخ ورود نمی‌تواند مساوی یا بعد از تاریخ خروج باشد.")
        
        overlapping_reservations = Reservation.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
        ).exclude(id=self.id)
        if overlapping_reservations.exists():
            raise ValidationError("این اتاق برای بازه زمانی انتخاب شده قبلاً رزرو شده است.")

    def save(self, *args, **kwargs):
        """محاسبه قیمت و اعمال ولیدیشن هنگام ذخیره"""
        self.clean()  
        self.calculate_price()  
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.room} ({self.check_in} تا {self.check_out})"


class PaymentInfo(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, verbose_name="اطلاعات رزرو")
    discount_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="کد تخفیف")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    accepted_terms = models.BooleanField(default=False, verbose_name="تأیید قوانین و مقررات", blank=False)
    tracking_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد پیگیری", unique=True)
    discount_price = models.CharField(max_length=50, blank=True, null=True, verbose_name="قیمت با تخفیف")
    DISCOUNT_AMOUNT = 2000000

    def clean(self):
        """اعتبارسنجی پرداخت"""
        if not self.accepted_terms:
            raise ValidationError({"accepted_terms": "شما باید قوانین و مقررات را تأیید کنید."})
        if self.discount_code and self.discount_code != "OFF100":
            raise ValidationError({"discount_code": "کد تخفیف نامعتبر است."})

    def apply_discount(self):
        """نمایش دادن در پنل ادمین جنگو"""
        if self.discount_code == "OFF100" and self.reservation.total_price:
            discounted_price = self.reservation.total_price - self.DISCOUNT_AMOUNT  
            self.discount_price = str(discounted_price)  
            self.reservation.total_price = discounted_price 
            self.reservation.save()

    def get_discounted_price(self):
        """محاسبه قیمت تخفیف‌خورده"""
        if self.discount_code == "OFF100" and self.reservation.total_price:
            return self.reservation.total_price - self.DISCOUNT_AMOUNT
        return self.reservation.total_price


    def generate_tracking_code(self):
        """تولید کد پیگیری رندوم"""
        self.tracking_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def save(self, *args, **kwargs):
        """اضافه کردن کد پیگیری"""
        self.clean()
        if not self.tracking_code:
            self.generate_tracking_code()
        self.apply_discount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"پرداخت برای {self.reservation.last_name} ({self.reservation.room})"