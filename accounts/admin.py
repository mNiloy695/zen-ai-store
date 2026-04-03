from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user__id', 'name', 'phone_number', 'avatar')
    search_fields = ('user__email', 'name', 'phone_number')