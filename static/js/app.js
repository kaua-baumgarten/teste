const modal = document.getElementById("modal");

const lista = document.getElementById("lista-jogadores");

const pesquisa = document.getElementById("pesquisaModal");

let jogadoresAtuais = [];

let jogadoresSelecionados = [];

let botaoSelecionado = null;

let timeEscolhido = [];

let notasTime = [];


//ABRIR MODAL
function abrirModal(posicao, botao){

    botaoSelecionado = botao;

    modal.style.display = "flex";

    pesquisa.value = "";

   lista.innerHTML = "<p></p>";
    
};



//FECHAR MODAL
function fecharModal(){

    modal.style.display = "none";

}


//ESCOLHER JOGADOR
function escolherJogador(nome, clube, foto, nota){

    botaoSelecionado.innerHTML = `
        <img src="${foto}" class="foto-campo">
        <br>
        <br>
        <div class="nome-jogador">${nome}</div>

        <div class="clube-jogador">${clube}</div>

        <div class="nota-jogador">Nota: ${nota}</div>

    `;

    timeEscolhido.push(nome);
    notasTime.push(nota);

    atualizarOverall();
    fecharModal();

}

//ESCOLHER JOGADOR API
function escolherJogadorAPI(nome, clube, foto, nota){

    nota = parseFloat(nota);

    if(isNaN(nota)){
        nota = 75;
    }

    botaoSelecionado.innerHTML = `

        <img src="${foto}" class="foto-campo">

        <div class="nome-jogador">${nome}</div>

        <div class="clube-jogador">${clube}</div>

        <div class="nota-jogador">${nota.toFixed(1)}</div>

    `;

    timeEscolhido.push(nome);

    notasTime.push(nota);

    atualizarOverall();

    fecharModal();

}

//LIMPAR
function limparTime(){

    jogadoresSelecionados = [];

    document.querySelectorAll(".posicao").forEach(function(botao){

        if(botao.innerHTML === "Alisson" ||
           botao.innerHTML === "Haaland" ||
           botao.innerHTML === "Mbappé" ||
           botao.innerHTML === "Salah"){

            
        }

    });

    location.reload();

}

//OVERALL
function atualizarOverall(){

    let soma = 0;

    notasTime.forEach(function(nota){
        soma += nota;
    });

    let media = Math.round(soma / notasTime.length);

    document.getElementById("overall").innerHTML = media;

}

//async PESQUISAR API
async function pesquisarAPI(nome){

    nome = nome.trim();

    if(nome.length < 2){
        lista.innerHTML = "";
        return;
    }

    lista.innerHTML = "<p>Pesquisando...</p>";

    const resposta = await fetch("/buscar_jogador/?nome=" + nome);

    const dados = await resposta.json();

    lista.innerHTML = "";

    if(dados.jogadores.length === 0){
        lista.innerHTML = "<p>Nenhum jogador encontrado.</p>";
        return;
    }

    dados.jogadores.forEach(jogador=>{

        lista.innerHTML += `
            <div class="jogador"
            onclick="escolherJogadorAPI(
                '${jogador.nome}',
                '${jogador.time}',
                '${jogador.foto}',
                '75'
            )">

                <img src="${jogador.foto}" width="60">

                <strong>${jogador.nome}</strong><br>

                ${jogador.time}<br>

                ${jogador.posicao}

            </div>
        `;

    });

}

document.getElementById("btnPesquisar").addEventListener("click", function(){

    pesquisarAPI(pesquisa.value);

});

pesquisa.addEventListener("keydown", function(event){

    if(event.key === "Enter"){

        pesquisarAPI(pesquisa.value);

    }

});