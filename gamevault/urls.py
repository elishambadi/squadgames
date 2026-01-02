
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('game/<slug:slug>/', views.game_detail, name='game_detail'),
    path('create/', views.game_create, name='game_create'),
    path('game/<slug:slug>/edit/', views.game_edit, name='game_edit'),
]