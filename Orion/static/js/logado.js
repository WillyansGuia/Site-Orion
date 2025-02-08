async function agendarServico() {
    const servico = document.querySelector('#servico').value;
    const data = document.querySelector('#data').value;
    const horario = document.querySelector('#horario').value;
  
    // Validação básica dos campos
    if (!servico || !data || !horario) {
      Swal.fire({
        title: 'Atenção!',
        text: 'Preencha todos os campos corretamente',
        icon: 'warning',
        confirmButtonText: 'Ok',
        confirmButtonColor: '#3085d6'
      });
      return;
    }
  
    try {
      const response = await fetch('/api/agendamentos', {
        method: 'POST',
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
        // Mostra mensagem de sucesso
        Swal.fire({
          title: 'Sucesso!',
          text: 'Agendamento realizado com sucesso!',
          icon: 'success',
          timer: 2000,
          showConfirmButton: false,
          timerProgressBar: true,
          didOpen: () => {
            Swal.showLoading();
          }
        }).then(() => {
          window.location.reload(); // Recarrega a página para atualizar o histórico
        });
      } else {
        // Mostra mensagem de erro
        Swal.fire({
          title: 'Erro!',
          text: dataResponse.error || 'Erro ao realizar agendamento',
          icon: 'error',
          confirmButtonText: 'Ok',
          confirmButtonColor: '#3085d6'
        });
      }
    } catch (error) {
      // Mostra mensagem de erro em caso de exceção
      Swal.fire({
        title: 'Erro!',
        text: error.message || 'Erro ao realizar agendamento',
        icon: 'error',
        confirmButtonText: 'Ok',
        confirmButtonColor: '#3085d6'
      });
    }
  }

  // Função para fazer logout
function fazerLogout() {
  fetch('/api/logout', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
  })
  .then(response => response.json())
  .then(data => {
      if (data.message === 'Logout realizado com sucesso') {
        window.location.href = '/login'; 
      } else {
          Swal.fire({
              title: 'Erro!',
              text: data.error || 'Erro ao fazer logout',
              icon: 'error',
              confirmButtonText: 'Ok',
              confirmButtonColor: '#3085d6'
          });
      }
  })
  .catch(error => {
      Swal.fire({
          title: 'Erro!',
          text: error.message || 'Erro ao fazer logout',
          icon: 'error',
          confirmButtonText: 'Ok',
          confirmButtonColor: '#3085d6'
      });
  });
}

// Adiciona o evento de clique ao botão de logout
document.getElementById('btn-logout').addEventListener('click', function(event) {
  event.preventDefault(); // Impede o comportamento padrão do link
  fazerLogout(); // Chama a função de logout
});