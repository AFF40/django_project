from django.contrib import admin
from .models import User, Restaurant, Menu, Product
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Product)

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_owner',)}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_owner')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_owner')

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)
