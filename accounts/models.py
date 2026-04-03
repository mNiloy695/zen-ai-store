from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser,BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        #validation for superuser
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self.create_user(email,password,**extra_fields)
    

class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()
    
    def __str__(self):
        return f'email : {self.email} - name  : {self.first_name} {self.last_name} and id is {self.id}'
    
    

class UserProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    avatar=models.ImageField(upload_to='avatars/',blank=True,null=True)
    name=models.CharField(max_length=110,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    phone_number=models.CharField(max_length=20,blank=True,null=True)
    
    def __str__(self):
        return f'Profile of {self.user.email}'