from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import UserProfile

User=get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['email','first_name','last_name','password','confirm_password']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    
    def validate(self,attrs):
        password=attrs.get('password')
        confirm_password=attrs.pop('confirm_password')
        email=attrs.get('email')
        
        if not password:
            raise serializers.ValidationError("Password is required")
        
        if not confirm_password:
            raise serializers.ValidationError("Confirm password is required")
        
        if password !=confirm_password:
            raise serializers.ValidationError("Password and confirm password do not match")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists")
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
   
    
    class Meta:
        model=UserProfile
        fields=['id','name','phone_number','avatar','address']
        


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    


