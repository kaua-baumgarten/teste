from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Jogador
import requests
from datetime import date, datetime

def index(request):

    jogadores = Jogador.objects.all()

    return render(request, 'jogadores/index.html', {
        'jogadores': jogadores
    })


def adicionar(request):

    if request.method == 'POST':

        nome = request.POST['nome']

        url = f'https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={nome}'

        resposta = requests.get(url)
        dados = resposta.json()

        time = 'Não encontrado'
        nacionalidade = 'Não encontrada'

        if dados['player']:

            jogador = dados['player'][0]

            time = jogador.get('strTeam', 'Não encontrado')
            nacionalidade = jogador.get('strNationality', 'Não encontrada')

        Jogador.objects.create(
            nome=nome,
            time=time,
            nacionalidade=nacionalidade
        )

        return redirect('/')

    return render(request, 'jogadores/adicionar.html')


def editar(request, id):

    jogador = get_object_or_404(Jogador, id=id)

    if request.method == 'POST':

        jogador.nome = request.POST['nome']
        jogador.time = request.POST['time']
        jogador.nacionalidade = request.POST['nacionalidade']

        jogador.save()

        return redirect('/')

    return render(request, 'jogadores/editar.html', {
        'jogador': jogador
    })


def deletar(request, id):

    jogador = get_object_or_404(Jogador, id=id)

    jogador.delete()

    return redirect('/')


def search_players(request):
    q = request.GET.get('q') or request.GET.get('player')
    if not q:
        return JsonResponse({'error': 'Parâmetro "q" (nome do jogador) é obrigatório.'}, status=400)

    url = f'https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={q}'

    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
    except Exception:
        return JsonResponse({'error': 'Falha ao conectar à API externa.'}, status=502)

    players = []
    seen_ids = set()

    def add_player_from_record(p):
        idp = p.get('idPlayer')
        if idp and idp in seen_ids:
            return
        if idp:
            seen_ids.add(idp)

        nome = p.get('strPlayer')
        foto = p.get('strThumb') or p.get('strCutout') or p.get('strRender')
        nacionalidade = p.get('strNationality')
        clube = p.get('strTeam')
        posicao = p.get('strPosition')

        idade = None
        date_str = p.get('dateBorn')
        if date_str:
            try:
                born = datetime.strptime(date_str, '%Y-%m-%d').date()
                today = date.today()
                idade = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            except Exception:
                idade = None

        players.append({
            'id': idp,
            'nome': nome,
            'foto': foto,
            'nacionalidade': nacionalidade,
            'idade': idade,
            'clube': clube,
            'posicao': posicao,
        })

    if data and data.get('player'):
        for p in data.get('player'):
            add_player_from_record(p)

    # Se poucos resultados, tentar buscas adicionais por tokens do nome
    if len(players) <= 1 and q and ' ' in q:
        tokens = [t.strip() for t in q.split() if len(t.strip()) > 2]
        for token in tokens:
            try:
                resp2 = requests.get(f'https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={token}', timeout=5)
                data2 = resp2.json()
                if data2 and data2.get('player'):
                    for p2 in data2.get('player'):
                        add_player_from_record(p2)
            except Exception:
                pass

    return JsonResponse({'players': players})


def search_page(request):
    saved = Jogador.objects.all()
    return render(request, 'jogadores/search.html', {
        'saved': saved
    })


@csrf_exempt
def save_player(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    data = request.POST or request.body

    # aceitar tanto form-encoded quanto JSON
    nome = request.POST.get('nome') or None
    time = request.POST.get('clube') or request.POST.get('time') or None
    nacionalidade = request.POST.get('nacionalidade') or None
    foto = request.POST.get('foto') or None
    idade = request.POST.get('idade') or None
    posicao = request.POST.get('posicao') or None

    if not nome:
        return JsonResponse({'error': 'Nome obrigatório.'}, status=400)

    jogador = Jogador.objects.create(
        nome=nome,
        time=time or 'Não informado',
        nacionalidade=nacionalidade or 'Não informada',
        foto=foto or None,
        idade=(int(idade) if idade and str(idade).isdigit() else None),
        posicao=posicao or ''
    )

    return JsonResponse({'id': jogador.id, 'nome': jogador.nome})


@csrf_exempt
def remove_player(request, id):
    if request.method not in ('POST', 'DELETE'):
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    jogador = get_object_or_404(Jogador, id=id)
    jogador.delete()
    return JsonResponse({'status': 'ok'})