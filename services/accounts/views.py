from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin, IsSuperAdmin, IsCustomerOrReadOnly

# 4a. Extend the JWT serializer to include 'role'
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 4b. User management API (super-admin only)
class UserViewSet(viewsets.ModelViewSet):
    """
    SuperAdmin can create/list/update/delete users.
    Admin can list and retrieve.
    Customer can only retrieve/list themselves (SAFE_METHODS).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCustomerOrReadOnly]

    def get_permissions(self):
        # Only SuperAdmin can create or delete users
        if self.action in ['create', 'destroy', 'partial_update', 'update']:
            permission_classes = [IsSuperAdmin]
        elif self.action in ['list']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsCustomerOrReadOnly]
        return [perm() for perm in permission_classes]

    def list(self, request, *args, **kwargs):
        # Admin sees all users; customer sees only self
        if request.user.role == User.ROLE_CUSTOMER:
            self.queryset = self.queryset.filter(pk=request.user.pk)
        return super().list(request, *args, **kwargs)
