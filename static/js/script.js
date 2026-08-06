const botoes = document.querySelectorAll(".posicao");
let botaoSelecionado = null;
botoes.forEach(botao => {

    botao.addEventListener("click", () => {

        alert("Você clicou em " + botao.innerText);

    });

});
