from django.contrib import admin
from .models import User, Restaurant, Menu, Product
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Product)

# Obtener el modelo de usuario personalizado
User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # Añade el campo `is_owner` a los campos que se muestran en el admin
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_owner',)}),
    )

    # Si quieres que `is_owner` aparezca en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_owner')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_owner')

# Desregistrar el User por defecto (si está registrado) y registrar el personalizado
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)
