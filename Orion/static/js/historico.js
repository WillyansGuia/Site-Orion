    document.addEventListener('DOMContentLoaded', carregarAgendamentos);

    let agendamentoEditando = null;

    // Função para carregar os agendamentos
    let data = null; // Variável global para armazenar os agendamentos

    async function carregarAgendamentos() {
        try {
            const response = await fetch('/api/agendamentos');
            data = await response.json(); // Armazena os agendamentos na variável global

            if (response.ok) {
                const tbody = document.querySelector('#tabela-agendamentos tbody');
                tbody.innerHTML = ''; // Limpa a tabela

                data.agendamentos.forEach(agendamento => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${agendamento.servico}</td>
                        <td>${agendamento.data}</td>
                        <td>${agendamento.horario}</td>
                        <td>
                            <button onclick="abrirModalEditar(${agendamento.id})" class="btn-acao btn-editar">Editar</button>
                            <button onclick="excluirAgendamento(${agendamento.id})" class="btn-acao btn-editar">Excluir</button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            } else {
                Swal.fire({
                    title: 'Erro!',
                    text: data.error || 'Erro ao carregar agendamentos',
                    icon: 'error',
                    confirmButtonText: 'Ok',
                    confirmButtonColor: '#3085d6'
                });
            }
        } catch (error) {
            Swal.fire({
                title: 'Erro!',
                text: error.message || 'Erro ao carregar agendamentos',
                icon: 'error',
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3085d6'
            });
        }
    }

    // Carrega os agendamentos quando a página é carregada
    document.addEventListener('DOMContentLoaded', carregarAgendamentos);



    // Função para abrir o modal de edição
    function abrirModalEditar(id) {
        if (!data || !data.agendamentos) {
            Swal.fire({
                title: 'Erro!',
                text: 'Agendamentos não carregados',
                icon: 'error',
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3085d6'
            });
            return;
        }
    
        // Busca o agendamento pelo ID
        const agendamento = data.agendamentos.find(a => a.id === id);
        if (agendamento) {
            agendamentoEditando = agendamento; // Armazena o agendamento que está sendo editado
    
            // Preenche os campos do modal com os dados do agendamento
            document.querySelector('#editar-servico').value = agendamento.servico;
            document.querySelector('#editar-data').value = agendamento.data.split('T')[0]; // Formata a data
            document.querySelector('#editar-horario').value = agendamento.horario;
    
            // Exibe o modal
            document.querySelector('#modal-editar').style.display = 'block';
        } else {
            Swal.fire({
                title: 'Erro!',
                text: 'Agendamento não encontrado',
                icon: 'error',
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3085d6'
            });
        }
    }

    // Função para fechar o modal
    function fecharModal() {
        document.querySelector('#modal-editar').style.display = 'none';
        agendamentoEditando = null; // Limpa o agendamento que estava sendo editado
    }

    // Função para salvar a edição
    async function salvarEdicao() {
        if (!agendamentoEditando) {
            Swal.fire({
                title: 'Erro!',
                text: 'Nenhum agendamento selecionado para editar',
                icon: 'error',
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3085d6'
            });
            return;
        }

        const servico = document.querySelector('#editar-servico').value;
        const data = document.querySelector('#editar-data').value;
        const horario = document.querySelector('#editar-horario').value;

        try {
            const response = await fetch(`/api/agendamentos/${agendamentoEditando.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    servico: servico,
                    data: data,
                    horario: horario
                })
            });

            const dataResponse = await response.json();

            if (response.ok) {
                Swal.fire({
                    title: 'Sucesso!',
                    text: 'Agendamento atualizado com sucesso!',
                    icon: 'success',
                    timer: 2000,
                    showConfirmButton: false,
                    timerProgressBar: true,
                    didOpen: () => {
                        Swal.showLoading();
                    }
                }).then(() => {
                    fecharModal();
                    carregarAgendamentos(); // Recarrega a lista de agendamentos
                });
            } else {
                Swal.fire({
                    title: 'Erro!',
                    text: dataResponse.error || 'Erro ao atualizar agendamento',
                    icon: 'error',
                    confirmButtonText: 'Ok',
                    confirmButtonColor: '#3085d6'
                });
            }
        } catch (error) {
            Swal.fire({
                title: 'Erro!',
                text: error.message || 'Erro ao atualizar agendamento',
                icon: 'error',
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3085d6'
            });
        }
    }

    // Função para excluir um agendamento
    async function excluirAgendamento(id) {
        try {
            const response = await fetch(`/api/agendamentos/${id}`, {
                method: 'DELETE'
            });

            const dataResponse = await response.json();

            if (response.ok) {
                Swal.fire({
                    title: 'Sucesso!',
                    text: 'Agendamento excluído com sucesso!',
                    icon: 'success',
                    timer: 2000,
                    showConfirmButton: false,
                    timerProgressBar: true,
                    didOpen: () => {
                        Swal.showLoading();
                    }
                }).then(() => {
                    carregarAgendamentos(); // Recarrega a lista de agendamentos
                });
            } else {
                Swal.fire({
                    title: 'Erro!',
                    text: dataResponse.error || 'Erro ao excluir agendamento',
                    icon: 'error',
                    confirmButtonText: 'Ok',
                    confirmButtonColor: '#3085d6'
                });
            }
        } catch (error) {
            Swal.fire({
                title: 'Erro!',
                text: error.message || 'Erro ao excluir agendamento',
                icon: 'error',
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3085d6'
            });
        }
    }