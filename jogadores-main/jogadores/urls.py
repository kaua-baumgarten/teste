from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('api/players/', views.search_players),
    path('buscar/', views.search_page),
    path('guardar/', views.save_player),
    path('remover/<int:id>/', views.remove_player),
]