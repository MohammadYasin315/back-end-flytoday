from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer, UserReservationSerializer
from .models import UserProfile
from .permissions import IsOwner
from reservations.models import Reservation

class RegisterView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        srz_data = RegisterSerializer(data=request.data)
        if srz_data.is_valid():
            user = srz_data.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "ثبت نام موفقیت آمیز بود",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        srz_data = LoginSerializer(data=request.data)
        if srz_data.is_valid():
            user = srz_data.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'ورود موفقیت آمیز بود',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },   status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated,]

#     def post(self, request):
#         refresh_token = request.data.get("refresh")
#         if not refresh_token:
#             return Response({"error": "توکن رفرش را وارد کنید"}, status=status.HTTP_400_BAD_REQUEST)

#         token = RefreshToken(refresh_token)
#         token.blacklist()
#         return Response({"message": "خروج موفقیت آمیز بود"}, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]
    queryset = UserProfile.objects.all()

    def list(self, request):
        if not request.user.is_staff:
            return Response({"detail": "شما اجازه دیدن این لیست را ندارید."}, status=403)
        
        srz_data = ProfileSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data)


    def retrieve(self, request, pk=None):
        profile = get_object_or_404(UserProfile, pk=pk)
        self.check_object_permissions(request, profile)
        srz_data = ProfileSerializer(profile)
        return Response(srz_data.data)


    def update(self, request, pk=None):
        profile = get_object_or_404(UserProfile, pk=pk)
        self.check_object_permissions(request, profile)  
        srz_data = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data)
        return Response(srz_data.errors, status=400)


    # def destroy(self, request, pk=None):
    #     profile = get_object_or_404(UserProfile, pk=pk)
    #     self.check_object_permissions(request, profile)  
    #     profile.delete()
    #     return Response({"detail": "حذف حساب کاربری موفقیت آمیز بود"}, status=204)


    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'destroy']:
            self.permission_classes += [IsOwner]
        return super().get_permissions()


class UserReservationsView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        """نمایش رزروهای کاربر جاری"""
        user_profile = request.user.profile
        reservations = Reservation.objects.filter(user=user_profile) 
        serializer = UserReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    