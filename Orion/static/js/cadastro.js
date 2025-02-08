let nome = document.querySelector('#nome');
let labelNome = document.querySelector('#labelNome');
let validNome = false;

let usuario = document.querySelector('#email');
let labelUsuario = document.querySelector('#labelEmail');
let validUsuario = false;

let senha = document.querySelector('#senha');
let labelSenha = document.querySelector('#labelSenha');
let validSenha = false;

let confirmSenha = document.querySelector('#confirmSenha');
let labelConfirmSenha = document.querySelector('#labelConfirmSenha');
let validConfirmSenha = false;

let bairro = document.querySelector('#bairro');          
let labelBairro = document.querySelector('#labelBairro');
let validBairro = false;

let rua = document.querySelector('#rua');                
let labelRua = document.querySelector('#labelRua');
let validRua = false;

let numero = document.querySelector('#numero');                
let labelNumero = document.querySelector('#labelNumero');
let validNumero = false;

let cep = document.querySelector('#cep');                
let labelCEP = document.querySelector('#labelCEP');
let validCEP = false;

let msgError = document.querySelector('#msgError');
let msgSuccess = document.querySelector('#msgSuccess');

// Validação do nome
nome.addEventListener('keyup', () => {
  if (nome.value.length <= 2) {
    labelNome.setAttribute('style', 'color: red');
    labelNome.innerHTML = 'Nome *Insira no mínimo 3 caracteres';
    nome.setAttribute('style', 'border-color: red');
    validNome = false;
  } else {
    labelNome.setAttribute('style', 'color: green');
    labelNome.innerHTML = 'Nome';
    nome.setAttribute('style', 'border-color: green');
    validNome = true;
  }
});

// Validação do email
usuario.addEventListener('keyup', () => {
  if (usuario.value.length <= 4) {
    labelUsuario.setAttribute('style', 'color: red');
    labelUsuario.innerHTML = 'Email *Insira no mínimo 5 caracteres';
    usuario.setAttribute('style', 'border-color: red');
    validUsuario = false;
  } else {
    labelUsuario.setAttribute('style', 'color: green');
    labelUsuario.innerHTML = 'Email';
    usuario.setAttribute('style', 'border-color: green');
    validUsuario = true;
  }
});

// Validação da senha
senha.addEventListener('keyup', () => {
  if (senha.value.length <= 5) {
    labelSenha.setAttribute('style', 'color: red');
    labelSenha.innerHTML = 'Senha *Insira no mínimo 6 caracteres';
    senha.setAttribute('style', 'border-color: red');
    validSenha = false;
  } else {
    labelSenha.setAttribute('style', 'color: green');
    labelSenha.innerHTML = 'Senha';
    senha.setAttribute('style', 'border-color: green');
    validSenha = true;
  }
});

// Validação da confirmação de senha
confirmSenha.addEventListener('keyup', () => {
  if (senha.value != confirmSenha.value) {
    labelConfirmSenha.setAttribute('style', 'color: red');
    labelConfirmSenha.innerHTML = 'Confirmar Senha *As senhas não conferem';
    confirmSenha.setAttribute('style', 'border-color: red');
    validConfirmSenha = false;
  } else {
    labelConfirmSenha.setAttribute('style', 'color: green');
    labelConfirmSenha.innerHTML = 'Confirmar Senha';
    confirmSenha.setAttribute('style', 'border-color: green');
    validConfirmSenha = true;
  }
});

// Validação do Bairro
bairro.addEventListener('keyup', () => {
  if (bairro.value.length <= 2) {
    labelBairro.setAttribute('style', 'color: red');
    labelBairro.innerHTML = 'Bairro *Insira no mínimo 3 caracteres';
    bairro.setAttribute('style', 'border-color: red');
    validBairro = false;
  } else {
    labelBairro.setAttribute('style', 'color: green');
    labelBairro.innerHTML = 'Bairro';
    bairro.setAttribute('style', 'border-color: green');
    validBairro = true;
  }
});

// Validação da Rua
rua.addEventListener('keyup', () => {
  if (rua.value.length < 1) {
    labelRua.setAttribute('style', 'color: red');
    labelRua.innerHTML = 'Rua *Insira no mínimo 3 caracteres';
    rua.setAttribute('style', 'border-color: red');
    validRua = false;
  } else {
    labelRua.setAttribute('style', 'color: green');
    labelRua.innerHTML = 'Rua';
    rua.setAttribute('style', 'border-color: green');
    validRua = true;
  }
});

// Validação do Numero
numero.addEventListener('keyup', () => {
  if (numero.value.length <= 2) {
    labelNumero.setAttribute('style', 'color: red');
    labelNumero.innerHTML = 'Numero *Insira no mínimo 3 caracteres';
    numero.setAttribute('style', 'border-color: red');
    validNumero = false;
  } else {
    labelNumero.setAttribute('style', 'color: green');
    labelNumero.innerHTML = 'Numero';
    numero.setAttribute('style', 'border-color: green');
    validNumero = true;
  }
});

// Validação do CEP
cep.addEventListener('keyup', () => {
  if (cep.value.length !== 8 || isNaN(cep.value)) {
    labelCEP.setAttribute('style', 'color: red');
    labelCEP.innerHTML = 'CEP *Insira um CEP válido (8 dígitos)';
    cep.setAttribute('style', 'border-color: red');
    validCEP = false;
  } else {
    labelCEP.setAttribute('style', 'color: green');
    labelCEP.innerHTML = 'CEP';
    cep.setAttribute('style', 'border-color: green');
    validCEP = true;
  }
});

async function cadastrar() {
  if (validNome && validUsuario && validSenha && validConfirmSenha && validBairro && validRua && validCEP) {
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: nome.value,
          email: usuario.value,
          password: senha.value,
          bairro: bairro.value,  
          rua: rua.value,    
          numero: numero.value,    
          cep: cep.value         
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Mostra mensagem de sucesso
        Swal.fire({
          title: 'Sucesso!',
          text: 'Usuário cadastrado com sucesso!',
          icon: 'success',
          timer: 2000,
          showConfirmButton: false,
          timerProgressBar: true,
          didOpen: () => {
            Swal.showLoading()
          }
        }).then(() => {
          window.location.href = '/login';
        });
      } else {
        // Mostra mensagem de erro
        Swal.fire({
          title: 'Erro!',
          text: data.error || 'Erro ao cadastrar usuário',
          icon: 'error',
          confirmButtonText: 'Ok',
          confirmButtonColor: '#3085d6'
        });
      }
    } catch (error) {
      // Mostra mensagem de erro em caso de exceção
      Swal.fire({
        title: 'Erro!',
        text: error.message || 'Erro ao cadastrar usuário',
        icon: 'error',
        confirmButtonText: 'Ok',
        confirmButtonColor: '#3085d6'
      });
    }
  } else {
    // Mostra mensagem de erro quando campos não estão validados
    Swal.fire({
      title: 'Atenção!',
      text: 'Preencha todos os campos corretamente',
      icon: 'warning',
      confirmButtonText: 'Ok',
      confirmButtonColor: '#3085d6'
    });
  }
}