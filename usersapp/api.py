from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework import status

# API to get user profile details
class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensures user must be logged in

    def get(self, request):
        user = request.user  # The authenticated user
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    
class UserListAPI(APIView):
    permission_classes = [IsAuthenticated]

    # Get all users (already implemented)
    def get(self, request):
        users = CustomUser.objects.all().values('id', 'username')
        return Response(list(users))

    # Create a new user
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)