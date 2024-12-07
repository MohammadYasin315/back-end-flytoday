from django.urls import path
from .views import CityListView


app_name = 'home'
urlpatterns = [
    path('cities/', CityListView.as_view(), name='city'),
]
