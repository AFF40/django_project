from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from urllib.parse import urlparse, parse_qs

class User(AbstractUser):
    is_owner = models.BooleanField(default=False)  # Agregar el campo is_owner
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='management_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='management_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location_url = models.URLField()  # URL que contiene la latitud y longitud
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')

    def __str__(self):
        return self.name

    def get_latitude(self):
        parsed_url = urlparse(self.location_url)
        query_params = parse_qs(parsed_url.query)
        return float(query_params.get('lat', [0])[0])

    def get_longitude(self):
        parsed_url = urlparse(self.location_url)
        query_params = parse_qs(parsed_url.query)
        return float(query_params.get('lng', [0])[0])

    def clean(self):
        # Validación personalizada: verificar que la URL contenga latitud y longitud
        parsed_url = urlparse(self.location_url)
        query_params = parse_qs(parsed_url.query)
        if 'lat' not in query_params or 'lng' not in query_params:
            raise ValidationError('La URL de ubicación debe contener parámetros de latitud y longitud.')

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    def clean(self):
        # Validación personalizada: el precio no puede ser negativo
        if self.price < 0:
            raise ValidationError('El precio no puede ser negativo.')
