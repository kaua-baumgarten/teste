import requests


URL_BUSCA = "https://www.thesportsdb.com/api/v1/json/123/searchplayers.php"

URL_STATS = "https://www.thesportsdb.com/api/v1/json/123/lookupplayerstats.php"


def buscar_estatisticas(id_jogador):

    resposta = requests.get(
        URL_STATS,
        params={
            "id": id_jogador
        }
    )

    dados = resposta.json()

    print("ESTATÍSTICAS:", dados)

    return dados


def calcular_nota(gols, jogos, assistencias, posicao):

    # Se não houver estatísticas
    if jogos <= 0:
        return 3.0

    gols_por_jogo = gols / jogos
    assistencias_por_jogo = assistencias / jogos

    participacoes = gols_por_jogo + assistencias_por_jogo


    # ==========================
    # ATAQUES
    # ==========================

    if posicao in [
        "Attacker",
        "Forward",
        "Striker",
        "Right Winger",
        "Left Winger"
    ]:

        if participacoes >= 1.0:
            nota = 5.0

        elif participacoes >= 0.75:
            nota = 4.5

        elif participacoes >= 0.50:
            nota = 4.0

        elif participacoes >= 0.30:
            nota = 3.5

        else:
            nota = 3.0


    # ==========================
    # MEIO CAMPO
    # ==========================

    elif posicao in [
        "Midfielder",
        "Central Midfielder",
        "Attacking Midfielder"
    ]:

        if participacoes >= 0.80:
            nota = 5.0

        elif participacoes >= 0.60:
            nota = 4.5

        elif participacoes >= 0.40:
            nota = 4.0

        elif participacoes >= 0.20:
            nota = 3.5

        else:
            nota = 3.0


    # ==========================
    # DEFESA
    # ==========================

    elif posicao in [
        "Defender",
        "Centre Back",
        "Left Back",
        "Right Back"
    ]:

        if jogos >= 100:
            nota = 5.0

        elif jogos >= 70:
            nota = 4.5

        elif jogos >= 40:
            nota = 4.0

        elif jogos >= 20:
            nota = 3.5

        else:
            nota = 3.0


    # ==========================
    # GOLEIRO
    # ==========================

    elif posicao == "Goalkeeper":

        if jogos >= 100:
            nota = 5.0

        elif jogos >= 70:
            nota = 4.5

        elif jogos >= 40:
            nota = 4.0

        elif jogos >= 20:
            nota = 3.5

        else:
            nota = 3.0


    else:

        nota = 3.0


    return nota

def buscar_jogadores(nome):

    resposta = requests.get(
        URL_BUSCA,
        params={
            "p": nome
        }
    )

    dados = resposta.json()

    jogadores = []


    if not dados.get("player"):

        return jogadores


    for jogador in dados["player"]:

        id_jogador = jogador.get("idPlayer")


        # ==========================
        # BUSCAR TODAS AS ESTATÍSTICAS
        # ==========================

        estatisticas = buscar_estatisticas(
            id_jogador
        )


        playerstats = estatisticas.get(
            "playerstats",
            []
        )


        # ==========================
        # TOTAIS DA CARREIRA
        # ==========================

        gols = 0

        jogos = 0

        assistencias = 0


        # ==========================
        # SOMAR TODAS AS TEMPORADAS
        # ==========================

        for estatistica in playerstats:

            tipo = estatistica.get(
                "strStatistic"
            )

            valor = estatistica.get(
                "strValue",
                "0"
            )


            try:

                valor = int(valor)

            except (ValueError, TypeError):

                valor = 0


            if tipo == "Goals":

                gols += valor


            elif tipo == "Appearances":

                jogos += valor


            elif tipo == "Assists":

                assistencias += valor


        # ==========================
        # CALCULAR NOTA
        # ==========================

        posicao = jogador.get(
            "strPosition"
        )


        nota = calcular_nota(
            gols,
            jogos,
            assistencias,
            posicao
        )


        # ==========================
        # JOGADOR
        # ==========================

        jogadores.append({

            "id": id_jogador,

            "nome": jogador.get(
                "strPlayer"
            ),

            "time": jogador.get(
                "strTeam"
            ),

            "nacionalidade": jogador.get(
                "strNationality"
            ),

            "posicao": posicao,

            "foto": jogador.get(
                "strThumb"
            ),

            "gols": gols,

            "jogos": jogos,

            "assistencias": assistencias,

            "nota": nota

        })


    return jogadores