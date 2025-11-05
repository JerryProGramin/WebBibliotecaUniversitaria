# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class SaludoAPIView(APIView):
    def get(self, request):
        return Response({"message": "Hola desde la API"})
