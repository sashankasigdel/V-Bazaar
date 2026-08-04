from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from .serializers import (
    CustomTokenObtainPairSerializer, RegisterSerializer,
    UserSerializer, CustomerProfileSerializer, ChangePasswordSerializer
)
from .models import CustomerProfile

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def google_auth(request):
    credential = request.data.get('credential')
    if not credential:
        return Response({'error': 'Missing credential.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payload = google_id_token.verify_oauth2_token(
            credential, google_requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        return Response({'error': 'Invalid Google token.'}, status=status.HTTP_400_BAD_REQUEST)

    if not payload.get('email_verified'):
        return Response({'error': 'Google email is not verified.'}, status=status.HTTP_400_BAD_REQUEST)

    email = payload['email']
    user = User.objects.filter(email=email).first()

    if not user:
        role = request.data.get('role')
        if role not in (User.Role.CUSTOMER, User.Role.BUSINESS_OWNER):
            role = User.Role.CUSTOMER

        base_username = email.split('@')[0]
        username = base_username
        suffix = 1
        while User.objects.filter(username=username).exists():
            suffix += 1
            username = f'{base_username}{suffix}'

        user = User(
            email=email,
            username=username,
            first_name=payload.get('given_name', ''),
            last_name=payload.get('family_name', ''),
            role=role,
            is_verified=True,
        )
        user.set_unusable_password()
        user.save()
        if user.is_customer:
            CustomerProfile.objects.create(user=user)

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password updated successfully.'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully.'})
    except Exception:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def saved_businesses(request):
    from apps.businesses.serializers import BusinessListSerializer
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    businesses = profile.saved_businesses.all()
    serializer = BusinessListSerializer(businesses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_save_business(request, business_id):
    from apps.businesses.models import Business
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    try:
        business = Business.objects.get(id=business_id)
        if business in profile.saved_businesses.all():
            profile.saved_businesses.remove(business)
            return Response({'saved': False})
        else:
            profile.saved_businesses.add(business)
            return Response({'saved': True})
    except Business.DoesNotExist:
        return Response({'error': 'Business not found.'}, status=status.HTTP_404_NOT_FOUND)
