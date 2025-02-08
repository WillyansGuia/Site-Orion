const historico = [];

function agendarServico() {
    const servico = document.getElementById('servico').value;
    const data = document.getElementById('data').value;
    if (servico && data) {
        historico.push(`Serviço: ${servico}, Data: ${data}`);
        atualizarHistorico();
        alert('Serviço agendado com sucesso!');
    } else {
        alert('Por favor, preencha todos os campos.');
    }
}

function comprarProduto(produto, preco) {
    historico.push(`Produto: ${produto}, Preço: R$ ${preco}`);
    atualizarHistorico();
    alert(`${produto} comprado com sucesso!`);
}

function enviarMensagem() {
    const mensagem = document.getElementById('mensagem').value;
    if (mensagem) {
        historico.push(`Mensagem enviada: ${mensagem}`);
        atualizarHistorico();
        alert('Mensagem enviada com sucesso!');
    } else {
        alert('Por favor, escreva uma mensagem.');
    }
}

function atualizarHistorico() {
    const historicoLista = document.getElementById('historico-lista');
    historicoLista.innerHTML = '';
    historico.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        historicoLista.appendChild(li);
    });
}
