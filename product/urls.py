from django.urls import path,include
from .views import ProductView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('list', ProductView, basename='product')
urlpatterns = [
    path('', include(router.urls)),
]
