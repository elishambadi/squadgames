"""
URL configuration for gameapp project.

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
from django.urls import path, include
from django.shortcuts import render

from gamevault import views as  gamevault_views

urlpatterns = [
    path('', lambda request: render(request, 'gamevault/landing.html'), name='home'),  # Home page shows game list
    path('admin/', admin.site.urls),
    path('games/', include('gamevault.urls')),
    path('login/', gamevault_views.user_login, name='login'),
    path('register/', gamevault_views.user_register, name='register'),
    path('logout/', gamevault_views.user_logout, name='logout'),
]
