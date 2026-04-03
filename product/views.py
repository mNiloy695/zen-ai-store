from django.shortcuts import render

from product.tasks import process_product
from .serializers import ProductSerializer
from .models import Product
from rest_framework import viewsets
from rest_framework import permissions
# Create your views here.

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
    

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('user').all()
    serializer_class = ProductSerializer
    permission_classes = [CustomPermission]
    
    def perform_create(self, serializer):
        product=serializer.save(user=self.request.user)
        process_product.delay(product.id)
        
        
    def get_queryset(self):
       user=self.request.user
       if user.is_superuser:
           return self.queryset
       return self.queryset.filter(user=user)