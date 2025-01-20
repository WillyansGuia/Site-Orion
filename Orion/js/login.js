let btn = document.querySelector('#btnMostrarSenha');
btn.addEventListener('click', () => {
    let inputSenha = document.querySelector('#senha');
    if (inputSenha.getAttribute('type') === 'password') {
        inputSenha.setAttribute('type', 'text');
    } else {
        inputSenha.setAttribute('type', 'password');
    }
});

function entrar() {
    let usuario = document.querySelector('#usuario');
    let senha = document.querySelector('#senha');
    let msgError = document.querySelector('#msgError');
    
    let userLabel = document.querySelector('#userLabel');
    let senhaLabel = document.querySelector('#senhaLabel');
    
    let listaUser = JSON.parse(localStorage.getItem('listaUser') || '[]');
    
    let userValid = { nome: 'abc', user: 'abc@abc', senha: '123456' };

    listaUser.forEach((item) => {
        if (usuario.value === item.userCad && senha.value === item.senhaCad) {
            userValid = {
                nome: item.nomeCad,
                user: item.userCad,
                senha: item.senhaCad
            };
        }
    });

    if (usuario.value === userValid.user && senha.value === userValid.senha) {
        window.location.href = 'usuario-logado.html';
        
        let mathRandom = Math.random().toString(16).substr(2);
        let token = mathRandom + mathRandom;

        localStorage.setItem('token', token);
        localStorage.setItem('userLogado', JSON.stringify(userValid));
    } else {

        userLabel.setAttribute('style', 'color: red');
        usuario.setAttribute('style', 'border-color: red');
        senhaLabel.setAttribute('style', 'color: red');
        senha.setAttribute('style', 'border-color: red');
        

        alert('Usuário ou senha incorretos');
        usuario.focus();
    }
}
