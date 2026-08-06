from django.shortcuts import render
from django.http import JsonResponse

from .services import buscar_jogadores


def index(request):
    return render(request, "index.html")


def buscar_jogador(request):

    nome = request.GET.get("nome", "")

    jogadores = buscar_jogadores(nome)

    return JsonResponse({
        "jogadores": jogadores
    })