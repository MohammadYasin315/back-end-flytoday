from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, PaymentInfoViewSet

app_name = 'reservations'

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'payments', PaymentInfoViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
