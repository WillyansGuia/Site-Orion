# Projeto Web Flask - Orion

## Tecnologias Utilizadas
- Python 3.8+
- Flask 3.0.0
- MySQL
- SQLAlchemy
- Flask-Migrate
- Flask-CORS
- Werkzeug
- PyMySQL

## Pré-requisitos
Antes de começar, certifique-se de ter instalado:
- Python 3.8 ou superior
- MySQL Server
- Git

## Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/WillyansGuia/Site-Orion.git
cd Site-Orion
cd Orion
```

### 2. Configure o Ambiente Virtual
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados MySQL

Acesse o MySQL e crie o banco de dados:
```sql
mysql -u root -p
CREATE DATABASE orion_db;
```

### 5. Configure o Arquivo .env
Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:
```
DB_USER=root
DB_PASSWORD=810502
DB_HOST=localhost
DB_PORT=3306
DB_NAME=orion_db
FLASK_SECRET_KEY=f590c6993b8947abee9fc82927e85d81
```

### 6. Initialize o Banco de Dados
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Execute o Projeto
```bash
python app.py
```
A aplicação estará disponível em `http://localhost:5000`

## Estrutura do Projeto
```
Orion/
├── app.py                 # Arquivo principal da aplicação
├── config/
│   └── database.py       # Configurações do banco de dados
├── controllers/
│   ├── agendamento_controller.py # Controlador de agendamentos
│   └── user_controller.py # Controlador de usuários
├── models/
│   ├── agendamento.py    # Modelo de agendamento
│   └── user.py           # Modelo de usuário
├── templates/            # Templates HTML
├── static/               # Arquivos estáticos (CSS, JS, imagens)
├── tests/                # Testes unitários
│   ├── test_agendamento_controller_editar.py
│   ├── test_agendamento_controller_excluir.py
│   ├── test_agendamento_controller_listar.py
│   ├── test_agendamento_controller.py
│   ├── test_user_controller_login.py
│   └── test_user_controller.py
├── requirements.txt      # Dependências do projeto
└── .env                  # Variáveis de ambiente
```

## Rotas da Aplicação
- `/` - Página inicial
- `/cadastro` - Página de cadastro de usuários
- `/login` - Página de login
- `/usuario-logado` - Área do usuário (requer autenticação)
- `/contato` - Página de contato
- `/servicos` - Página de serviços

## APIs
- `POST /api/users` - Criar novo usuário
- `POST /api/login` - Autenticar usuário
- `POST /api/agendamentos` - Criar novo agendamento
- `GET /api/agendamentos` - Listar agendamentos do usuário
- `PUT /api/agendamentos/<int:agendamento_id>` - Editar agendamento
- `DELETE /api/agendamentos/<int:agendamento_id>` - Excluir agendamento

## Testes Unitários

### Executando os Testes
Para executar todos os testes, utilize o seguinte comando:
```bash
python -m unittest discover tests/
```

### Testes Disponíveis
* **Testes de Usuário**
   * `test_user_controller.py`: Testes para criação de usuário e login.
   * `test_user_controller_login.py`: Testes específicos para autenticação de usuário.
* **Testes de Agendamento**
   * `test_agendamento_controller.py`: Testes para criação de agendamentos.
   * `test_agendamento_controller_editar.py`: Testes para edição de agendamentos.
   * `test_agendamento_controller_excluir.py`: Testes para exclusão de agendamentos.
   * `test_agendamento_controller_listar.py`: Testes para listagem de agendamentos.

### Exemplo de Execução de Testes Específicos
Para executar um teste específico, utilize o seguinte comando:
```bash
python -m unittest tests/test_user_controller.py
```

### Cobertura de Testes
Os testes cobrem as principais funcionalidades do sistema, incluindo:
* Criação e autenticação de usuários.
* Criação, edição, exclusão e listagem de agendamentos.
* Verificação de permissões e autenticação.

## Comandos Úteis

### Gerenciamento de Dependências
```bash
# Instalar dependências
pip install -r requirements.txt

# Atualizar requirements.txt
pip freeze > requirements.txt
```

### Banco de Dados
```bash
# Criar nova migration
flask db migrate -m "Descrição da alteração"

# Aplicar migrations
flask db upgrade

# Reverter última migration
flask db downgrade

# Acessar MySQL
mysql -u root -p
```
