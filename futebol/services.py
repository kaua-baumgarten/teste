import requests

URL = "https://www.thesportsdb.com/api/v1/json/123/searchplayers.php"


def buscar_jogadores(nome):

    resposta = requests.get(
        URL,
        params={"p": nome}
    )

    dados = resposta.json()

    jogadores = []

    if dados.get("player"):

        for jogador in dados["player"]:

            jogadores.append({

                "nome": jogador.get("strPlayer"),
                "clube": jogador.get("strTeam"),
                "posicao": jogador.get("strPosition"),
                "foto": jogador.get("strThumb")

            })

    return jogadores