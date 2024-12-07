from django.contrib import admin
from .models import Reservation, PaymentInfo


admin.site.register(Reservation)
admin.site.register(PaymentInfo)

