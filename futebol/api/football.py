import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"

def buscar_jogadores(nome, liga, temporada):

    url = f"{BASE_URL}/players"

    resposta = requests.get(
        url,
        headers=HEADERS,
        params={
            "search": nome,
            "league": liga,
            "season": temporada
        }
    )

    return resposta.json()