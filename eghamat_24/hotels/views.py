from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Min
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from accounts import serializers
from .models import Hotel, Review
from .serializers import HotelSerializer, HotelSummarySerializer, ReviewCreateSerializer

class HotelListView(APIView):
    def get(self, request):
        city_id = request.query_params.get('city_id')
        sort_by = request.query_params.get('sort_by')

        if not city_id:
            return Response(
                {"detail": "شناسه شهر وارد نشده است."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        hotels = Hotel.objects.filter(city_id=city_id).annotate(
            starting_price=Min('rooms__price_per_night')
        )

        if not hotels.exists():
            return Response(
                {"detail": "هتل شهر مورد نظر پیدا نشد."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if sort_by == 'price_asc':
            hotels = hotels.order_by('starting_price') 
        elif sort_by == 'price_desc':
            hotels = hotels.order_by('-starting_price')  
        elif sort_by == 'rating':
            hotels = hotels.order_by('-rating')

        srz_data = HotelSummarySerializer(hotels, many=True)
        return Response({"hotels": srz_data.data}, status=status.HTTP_200_OK)


class HotelDetailView(RetrieveAPIView): 
    serializer_class = HotelSerializer

    def get_object(self):
        hotel_id = self.kwargs.get('hotel_id')  
        return get_object_or_404(Hotel, id=hotel_id)  


class ReviewCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')  
        hotel = Hotel.objects.get(id=hotel_id)  
        serializer.save(user=self.request.user, hotel=hotel) 

    def create(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('hotel_id')
        try:
            Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return Response(
                {"detail": "هتل مورد نظر یافت نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().create(request, *args, **kwargs)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,] 
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def get_object(self):
        review = super().get_object()
        if review.user != self.request.user:
            raise PermissionDenied("شما اجازه ویرایش یا حذف این نظر را ندارید.")
        return review

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() 
        self.perform_destroy(instance) 
        return Response(
            {"detail": "نظر شما با موفقیت حذف شد"},
            status=status.HTTP_200_OK  
        )
    