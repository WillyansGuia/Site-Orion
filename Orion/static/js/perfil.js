document.addEventListener('DOMContentLoaded', carregarPerfil);

// Função para carregar os dados do perfil
async function carregarPerfil() {
    try {
        const response = await fetch('/api/perfil');
        const data = await response.json();

        if (response.ok) {
            // Preenche os campos do formulário com os dados do usuário
            document.querySelector('#editar-nome').value = data.user.name;
            document.querySelector('#editar-email').value = data.user.email;
            document.querySelector('#editar-bairro').value = data.user.bairro || '';
            document.querySelector('#editar-rua').value = data.user.rua || '';
            document.querySelector('#editar-numero').value = data.user.numero || '';
            document.querySelector('#editar-cep').value = data.user.cep || '';
        } else {
            Swal.fire({
                title: 'Erro!',
                text: data.error || 'Erro ao carregar perfil',
                icon: 'error',
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3085d6'
            });
        }
    } catch (error) {
        Swal.fire({
            title: 'Erro!',
            text: error.message || 'Erro ao carregar perfil',
            icon: 'error',
            confirmButtonText: 'Ok',
            confirmButtonColor: '#3085d6'
        });
    }
}

// Função para salvar a edição do perfil
async function salvarEdicaoPerfil() {
    const nome = document.querySelector('#editar-nome').value;
    const email = document.querySelector('#editar-email').value;
    const bairro = document.querySelector('#editar-bairro').value;
    const rua = document.querySelector('#editar-rua').value;
    const numero = document.querySelector('#editar-numero').value;
    const cep = document.querySelector('#editar-cep').value;

    try {
        const response = await fetch('/api/perfil', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: nome,
                email: email,
                bairro: bairro,
                rua: rua,
                numero: numero,
                cep: cep
            })
        });

        const dataResponse = await response.json();

        if (response.ok) {
            Swal.fire({
                title: 'Sucesso!',
                text: 'Perfil atualizado com sucesso!',
                icon: 'success',
                timer: 2000,
                showConfirmButton: false,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                }
            }).then(() => {
                window.location.reload(); // Recarrega a página para atualizar os dados
            });
        } else {
            Swal.fire({
                title: 'Erro!',
                text: dataResponse.error || 'Erro ao atualizar perfil',
                icon: 'error',
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3085d6'
            });
        }
    } catch (error) {
        Swal.fire({
            title: 'Erro!',
            text: error.message || 'Erro ao atualizar perfil',
            icon: 'error',
            confirmButtonText: 'Ok',
            confirmButtonColor: '#3085d6'
        });
    }
}