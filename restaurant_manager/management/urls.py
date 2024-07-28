from django.urls import path, include
from .views import login_view, register_view, logout_view, restaurant_map_view, view_menu, restaurant_settings
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuViewSet, ProductViewSet, UserViewSet, LoginView

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),  # Form-based login
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('map/', restaurant_map_view, name='restaurant_map'),
    path('view_menu/', view_menu, name='view_menu'),  # Añadir esta línea
    path('restaurant_settings/', restaurant_settings, name='restaurant_settings'),  # Añadir esta línea
    path('api/login/', LoginView.as_view(), name='api_login'),  # API login for DRF
]
