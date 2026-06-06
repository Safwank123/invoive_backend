from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'phone', 'role', 'is_approved', 'is_staff', 'created_at')
    list_filter = ('role', 'is_approved', 'is_staff')
    search_fields = ('username', 'email', 'name', 'phone')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_approved', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'name', 'password1', 'password2', 'role', 'is_approved', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ('created_at',)
