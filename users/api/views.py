# users/api/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": str(user.id),
            "phone": user.phone,
            "name": user.name if hasattr(user, "name") else "",
            "is_staff": user.is_staff,
        })