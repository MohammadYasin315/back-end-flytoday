from django.urls import path
from .views import HotelListView, HotelDetailView, ReviewCreateView, ReviewDetailView


app_name = 'hotels'
urlpatterns = [
    path('hotels/', HotelListView.as_view(), name='hotel'),
    path('hotels/<int:hotel_id>/', HotelDetailView.as_view(), name='hotel-detail'), 
    path('hotels/reviews/<int:hotel_id>/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]

