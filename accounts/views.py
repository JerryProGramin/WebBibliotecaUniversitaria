from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import StaffProfileSerializer

class StaffProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.staff_profile
        serializer = StaffProfileSerializer(profile)
        return Response(serializer.data)
