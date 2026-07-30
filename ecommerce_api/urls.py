"""
URL configuration for ecommerce_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from core.views import RegisterView, ProfileView, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import RegisterView, ProfileView, ChangePasswordView, LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth Endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/',include('products.urls')),
    path('api/',include('favorites.urls')),
    path('api/',include('favorites.urls')), 
    path('api/login/', LoginView.as_view(), name='login'),
    path('',include('cart.urls')),
    path('',include('orders.urls')),
    


]
