# lims_backend/accounts/views.py
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer, UserSerializer, ProfileUpdateSerializer, UserRoleUpdateSerializer
)
from .permissions import IsAdmin, IsAdminOrQAManager

User = get_user_model()

# Custom TokenObtainPairView if you want to include user data in response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add custom claims
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # attach user info
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
        })
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register
    Hanya Admin dapat mendaftarkan user baru.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class LogoutView(generics.GenericAPIView):
    """
    POST /api/auth/logout
    body: { "refresh": "<refresh_token>" }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail":"Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":"Invalid token or token required."}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/profile
    PUT /api/auth/profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = ProfileUpdateSerializer(self.request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(self.request.user).data)

# User management: list, update role/status, delete
class UserViewSet(viewsets.ModelViewSet):
    """
    GET /api/auth/users/           -> list semua user (Admin, QA Manager)
    PUT /api/auth/users/{id}/      -> update role/status (Admin)
    DELETE /api/auth/users/{id}/   -> hapus user (Admin)
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            permission_classes = [IsAuthenticated, IsAdminOrQAManager]
        elif self.action in ['update','partial_update','destroy']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]

    def get_serializer_class(self):
        if self.action in ['update','partial_update']:
            return UserRoleUpdateSerializer
        return UserSerializer

    # override destroy to allow hard delete by admin
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser:
            return Response({"detail":"Cannot delete superuser."}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)