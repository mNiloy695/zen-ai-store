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
class RegistrationView(APIView):
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

    def get(self, request):
        profile = self.get_profile(request.user)
        if not profile:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(profile, context={'request': request})
        data = serializer.data
        return Response(data)

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