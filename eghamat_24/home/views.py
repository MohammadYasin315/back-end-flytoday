from rest_framework.views import APIView
from rest_framework.response import Response
from .models import City
from .serializers import CitySerializer

class CityListView(APIView):
    def get(self, request):
        cities = City.objects.all()
        print(cities)
        srz_data = CitySerializer(cities, many=True)
        return Response(srz_data.data)
