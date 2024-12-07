from django.urls import path
from . import views
from .views import RegisterView, LoginView, UserReservationsView
from rest_framework import routers

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('reservations/', UserReservationsView.as_view(), name='user-reservations'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]


router = routers.SimpleRouter()
router.register('user', views.UserProfileViewSet)
urlpatterns += router.urls