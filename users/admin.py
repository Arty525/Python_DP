from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
