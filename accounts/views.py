from django.shortcuts import render
from .serializers import RegistrationSerializer,UserProfileSerializer,LoginSerializer
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example="salah1@gmail1.com"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, example="salah"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, example="uddin"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example="123"),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, example="123"),
            },
            required=['email', 'first_name', 'last_name', 'password', 'confirm_password'],
        ),
        responses={201: openapi.Response(
            description="Registration successful",
            examples={
                "application/json": {
                    "email": "salah1@gmail1.com",
                    "first_name": "salah",
                    "last_name": "uddin"
                }
            }
        )}
    )
    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_profile(self, user):
        return getattr(user, 'profile', None)

    @swagger_auto_schema(
        operation_description="Get user profile.\n\n**Requires Bearer token in Authorization header.**",
        responses={200: openapi.Response(
            description="Profile data",
            examples={
                "application/json": {
                    "id": 3,
                    "name": "SALAH UDDIN bro",
                    "phone_number": "01806779324",
                    "avatar": "http://127.0.0.1:8000/media/avatars/Screenshot_from_2026-01-29_12-05-14.png",
                    "address": "Dhaka Bangladesh (present now) 1"
                }
            }
        )},
        security=[{'Bearer': []}]
    )
    def get(self, request):
        profile = self.get_profile(request.user)
        if not profile:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(profile, context={'request': request})
        data = serializer.data
        return Response(data)

    @swagger_auto_schema(
        operation_description="Update user profile.\n\n**Requires Bearer token in Authorization header.**",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example="SALAH UDDIN bro"),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example="01806779324"),
                'avatar': openapi.Schema(type=openapi.TYPE_STRING, format='binary'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, example="Dhaka Bangladesh (present now) 1"),
            },
        ),
        responses={200: openapi.Response(
            description="Profile updated",
            examples={
                "application/json": {
                    "id": 3,
                    "name": "SALAH UDDIN bro",
                    "phone_number": "01806779324",
                    "avatar": "http://127.0.0.1:8000/media/avatars/Screenshot_from_2026-01-29_14-33-39.png",
                    "address": "Dhaka Bangladesh (present now) 1"
                }
            }
        )},
        security=[{'Bearer': []}]
    )
    def patch(self, request):
        profile = self.get_profile(request.user)
        if not profile:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data,status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example="salah1@gmail1.com"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example="123"),
            },
            required=['email', 'password'],
        ),
        responses={200: openapi.Response(
            description="Login successful",
            examples={
                "application/json": {
                    "refresh": "refresh_token_here",
                    "access": "access_token_here",
                    "user_data": {
                        "id": 3,
                        "email": "salah1@gmail1.com",
                        "first_name": "salah",
                        "last_name": "uddin"
                    }
                }
            }
        )}
    )
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']
            user=authenticate(request,email=email,password=password)
            if user is not None:
                refresh=RefreshToken.for_user(user)
                return Response({
                    'refresh':str(refresh),
                    'access':str(refresh.access_token),
                    "user_data":{
                        "id":user.id,
                        "email":user.email,
                        "first_name":user.first_name,
                        "last_name":user.last_name
                    }
                },status=status.HTTP_200_OK)
            return Response({"detail":"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, example="refresh_token_here"),
            },
            required=['refresh'],
        ),
        operation_description="Logout user (blacklist refresh token).\n\n**Requires Bearer token in Authorization header.**",
        responses={200: openapi.Response(
            description="Logout successful",
            examples={
                "application/json": {"detail": "Successfully logged out."}
            }
        )},
        security=[{'Bearer': []}]
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)