from django.urls import path

from . import views


urlpatterns = [

    path("", views.index, name="index"),

    path(
        "buscar_jogador/",
        views.buscar_jogador,
        name="buscar_jogador"
    ),

]