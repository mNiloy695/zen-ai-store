from django.shortcuts import render
from product.tasks import process_product
from .serializers import ProductSerializer, ProductUpdateSerializer,BatchUploadSerializer
from .models import Product
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from .utils import get_product_from_cache, log_execution_time
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        
        return obj.user == request.user
    
    

#read product names from file with generator
def read_product_names_from_file(file):
    for product_name in file:
        name = product_name.decode('utf-8').strip()
        if name:
            yield name


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('user').all()
    serializer_class = ProductSerializer
    permission_classes = [CustomPermission]
    pagination_class = CustomPagination
    # Add Bearer token security for all actions
    
    def perform_create(self, serializer):
        product=serializer.save(user=self.request.user)
        cache.delete(f"products_user_{self.request.user.id}")
        process_product.delay(product.id)
    
    def perform_update(self, serializer):
        product=serializer.save()
        cache.delete(f"products_user_{self.request.user.id}")
        process_product.delay(product.id)
        
    def perform_destroy(self, instance):
        cache.delete(f"products_user_{self.request.user.id}")
        instance.delete()
    
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer
        
    @swagger_auto_schema(
        method='post',
        operation_description="Batch upload products from a .txt file (one product name per line).\n\n**Requires Bearer token in Authorization header.**",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Text file (.txt) with one product name per line'),
            },
            required=['file'],
        ),
        responses={
            201: openapi.Response(
                description="Batch upload successful and processing",
                examples={
                    "application/json": {"message": "Batch upload successful and processing"}
                }
            ),
            400: openapi.Response(
                description="Invalid file or data",
                examples={
                    "application/json": {"file": ["This field is required."]}
                }
            )
        },
        security=[{'Bearer': []}]
    )
    @action(detail=False, methods=['post'])
    def batch_upload(self, request):
        serializer = BatchUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            for product_name in read_product_names_from_file(file):
                product = Product.objects.create(user=request.user, name=product_name)
                process_product.delay(product.id)
            delete_cache_key = f"products_user_{request.user.id}"
            cache.delete(delete_cache_key)
            return Response({"message": "Batch upload successful and processing"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @log_execution_time
    def get_queryset(self):
        # Short-circuit for drf-yasg schema generation to avoid AnonymousUser errors
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        return get_product_from_cache(user=user)


