// Função para fazer login
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

// Evento de mostrar/ocultar senha
let btnMostrarSenha = document.querySelector('#btnMostrarSenha');
btnMostrarSenha.addEventListener('click', () => {
    let inputSenha = document.querySelector('#senha');
    let eyeIcon = btnMostrarSenha.querySelector('i');
    
    if (inputSenha.type === 'password') {
        inputSenha.type = 'text';
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    } else {
        inputSenha.type = 'password';
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
});

// Evento para voltar a senha ao campo perder o foco
document.querySelector('#senha').addEventListener('blur', () => {
    let inputSenha = document.querySelector('#senha');
    let eyeIcon = btnMostrarSenha.querySelector('i');
    
    // Se o usuário sair do campo, volta para password
    if (inputSenha.type === 'text') {
        inputSenha.type = 'password';
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
});

// Evento de Enter para fazer login
document.querySelector('form').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault(); // Impede o comportamento padrão do formulário
        entrar(); // Chama a função de login
    }
});