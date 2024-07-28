from rest_framework import viewsets
from .models import Restaurant, Menu, Product, User
from .serializers import RestaurantSerializer, MenuSerializer, ProductSerializer, UserSerializer, LoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import re

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def restaurant_map_view(request):
    try:
        restaurants = Restaurant.objects.all()
        
        restaurant_locations = []
        for restaurant in restaurants:
            match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', restaurant.location_url)
            if match:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
                restaurant_locations.append({
                    'name': restaurant.name,
                    'latitude': latitude,
                    'longitude': longitude
                })
        
        user_restaurants = Restaurant.objects.filter(owner=request.user)
        is_owner = request.user.is_owner if request.user.is_authenticated else False
        
        print(f"User: {request.user.username}, is_owner: {is_owner}")
        for restaurant in user_restaurants:
            print(f"Restaurant: {restaurant.name}, Location: {restaurant.location_url}")

        return render(request, 'management/map.html', {
            'restaurant_locations': restaurant_locations,
            'is_owner': is_owner
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return render(request, 'management/map.html', {
            'restaurant_locations': [],
            'is_owner': False,
            'error': str(e)
        })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Attempting login for username: {username}")  
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(f"Login successful for username: {username}")  
                login(request, user)
                return redirect('restaurant_map')
            else:
                print(f"Login failed for username: {username}")  
                messages.error(request, 'Invalid username or password')
        else:
            print("Form submission invalid")  
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()
    return render(request, 'management/login.html', {'form': form})





def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('restaurant_map')  
    else:
        form = UserCreationForm()
    return render(request, 'management/register.html', {'form': form})

def restaurant_locations_view(request):
    restaurants = Restaurant.objects.all().values('name', 'location_url')
    data = [
        {
            'name': restaurant['name'],
            'latitude': Restaurant.objects.get(id=restaurant['id']).get_latitude(),
            'longitude': Restaurant.objects.get(id=restaurant['id']).get_longitude()
        }
        for restaurant in restaurants
    ]
    return JsonResponse(data, safe=False)

def logout_view(request):
    logout(request)
    return redirect('login')  

@login_required
def view_menu(request):
    return render(request, 'management/view_menu.html')

@login_required
def restaurant_settings(request):
    return render(request, 'management/restaurant_settings.html')
