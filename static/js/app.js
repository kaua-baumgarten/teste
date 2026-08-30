const modal = document.getElementById("modal");
const lista = document.getElementById("lista-jogadores");
const pesquisa = document.getElementById("pesquisaModal");

let botaoSelecionado = null;
let timeEscolhido = [];


// ==============================
// ABRIR MODAL
// ==============================

function abrirModal(posicao, botao) {

    botaoSelecionado = botao;

    modal.style.display = "flex";

    pesquisa.value = "";

    lista.innerHTML = "";

}


// ==============================
// FECHAR MODAL
// ==============================

function fecharModal() {

    modal.style.display = "none";

}


// ==============================
// ESCOLHER JOGADOR
// ==============================

function escolherJogadorAPI(
    nome,
    clube,
    foto,
    gols,
    jogos,
    assistencias,
    nota
) {

    if (!botaoSelecionado) {
        return;
    }

    botaoSelecionado.innerHTML = `

        <img src="${foto}" class="foto-campo">

        <div class="nome-jogador">
            ${nome}
        </div>

        <div class="clube-jogador">
            ${clube || "Sem clube"}
        </div>

        <div class="nota-jogador">
            ⭐ ${nota || 0}/5
        </div>

    `;


  timeEscolhido.push({

    nome: nome,

    gols: Number(gols) || 0,

    jogos: Number(jogos) || 0,

    assistencias: Number(assistencias) || 0,

    nota: Number(nota) || 0

});

atualizarMediaTime();


    fecharModal();

}


// ==============================
// LIMPAR TIME
// ==============================

function limparTime() {

    timeEscolhido = [];

    location.reload();

}


// ==============================
// PESQUISAR
// ==============================

async function pesquisarAPI(nome) {

    nome = nome.trim();

    if (nome.length < 2) {

        lista.innerHTML = "";

        return;
    }


    lista.innerHTML = "<p>Pesquisando...</p>";


    try {

        const resposta = await fetch(
            "/buscar_jogador/?nome=" + encodeURIComponent(nome)
        );


        const dados = await resposta.json();


        lista.innerHTML = "";


        if (!dados.jogadores || dados.jogadores.length === 0) {

            lista.innerHTML = "<p>Nenhum jogador encontrado.</p>";

            return;
        }


        dados.jogadores.forEach(jogador => {


            const card = document.createElement("div");

            card.className = "jogador";


            card.innerHTML = `

                <img
                    src="${jogador.foto}"
                    class="foto-jogador"
                >

                <div class="info-jogador">

                    <strong class="nome-jogador">
                        ${jogador.nome}
                    </strong>

                    <span class="clube-jogador">
                        ${jogador.time || "Sem clube"}
                    </span>

                    <span class="posicao-jogador">
                        ${jogador.posicao || "Posição desconhecida"}
                    </span>

                    <span class="nota-jogador">
                        ⭐ ${jogador.nota || 0}/5
                    </span>

                </div>

            `;


            card.addEventListener("click", function() {

                escolherJogadorAPI(

                    jogador.nome,

                    jogador.time,

                    jogador.foto,

                    jogador.gols,

                    jogador.jogos,

                    jogador.assistencias,

                    jogador.nota

                );

            });


            lista.appendChild(card);

        });


    } catch (erro) {

        console.error("ERRO:", erro);

        lista.innerHTML = "<p>Erro ao pesquisar jogador.</p>";

    }

}


// ==============================
// BOTÃO PESQUISAR
// ==============================

document
    .getElementById("btnPesquisar")
    .addEventListener("click", function() {

        pesquisarAPI(pesquisa.value);

    });


// ==============================
// ENTER
// ==============================

pesquisa.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        pesquisarAPI(pesquisa.value);

    }

});
function atualizarMediaTime() {

    const elemento = document.getElementById("overall");

    if (timeEscolhido.length === 0) {

        elemento.innerHTML = "0.0";

        return;
    }

    let soma = 0;

    timeEscolhido.forEach(function(jogador) {

        soma += Number(jogador.nota) || 0;

    });

    const media = soma / timeEscolhido.length;

    elemento.innerHTML = media.toFixed(1);

}