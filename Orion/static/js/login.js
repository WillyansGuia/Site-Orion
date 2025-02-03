async function entrar() {
    const usuario = document.querySelector('#usuario');
    const senha = document.querySelector('#senha');
    const msgError = document.querySelector('#msgError');
    const userLabel = document.querySelector('#userLabel');
    const senhaLabel = document.querySelector('#senhaLabel');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: usuario.value,
                password: senha.value
            })
        });
        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('userLogado', JSON.stringify(data.user));

            Swal.fire({
                title: 'Sucesso!',
                text: 'Login realizado com sucesso!',
                icon: 'success',
                timer: 2000,
                showConfirmButton: false,
                timerProgressBar: true
            }).then(() => {
                window.location.href = '/usuario-logado';
            });
        } else {
            userLabel.style.color = 'red';
            usuario.style.borderColor = 'red';
            senhaLabel.style.color = 'red';
            senha.style.borderColor = 'red';

            Swal.fire({
                title: 'Erro!',
                text: data.message || 'Usuário ou senha inválido',
                icon: 'error',
                confirmButtonText: 'Ok'
            });
        }
    } catch (error) {
        Swal.fire({
            title: 'Erro!',
            text: 'Erro ao conectar com o servidor',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
}

let btnMostrarSenha = document.querySelector('#btnMostrarSenha');
btnMostrarSenha.addEventListener('click', () => {
    let inputSenha = document.querySelector('#senha');
    inputSenha.type = inputSenha.type === 'password' ? 'text' : 'password';
});