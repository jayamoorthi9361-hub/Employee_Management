from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer
from .permissions import IsManager

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class CustomAuthToken(ObtainAuthToken):
    serializer_class = LoginSerializer # Use our custom serializer that checks email

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        if not user.is_approved:
            return Response({
                'error': 'Account not approved by manager yet.'
            }, status=status.HTTP_403_FORBIDDEN)
            
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'massage': 'Login successful',
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role,
            'is_approved': user.is_approved
        })

class PendingUsersView(generics.ListAPIView):
    """
    List all Key employees who are not approved yet.
    Only Managers can see this.
    """
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return User.objects.filter(role=User.EMPLOYEE, is_approved=False)

class ApproveUserView(APIView):
    """
    Approve a specific user.
    Only Managers can do this.
    """
    permission_classes = [IsManager]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk, role=User.EMPLOYEE)
            user.is_approved = True
            user.save()
            return Response({"message": f"User {user.username} approved successfully."})
        except User.DoesNotExist:
            return Response({"error": "User not found or not an employee."}, status=status.HTTP_404_NOT_FOUND)
