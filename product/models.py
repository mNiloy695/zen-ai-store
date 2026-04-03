from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.

class Product(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name=models.CharField(max_length=2000)
    description=models.TextField(null=True, blank=True)
    category=models.CharField(max_length=250, null=True, blank=True)
    
    def __str__(self):
        return f"id {self.id} - name: {self.name}"
    
    
    