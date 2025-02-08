from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from config.database import init_db, db
from controllers.user_controller import UserController
from controllers.agendamento_controller import AgendamentoController
from functools import wraps
from models.user import User  # Importe o modelo User

app = Flask(__name__)
CORS(app)

init_db(app)

migrate = Migrate(app, db)

# Chave secreta para gerenciar sessões
app.secret_key = 'chave-desenvolvimento'

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rotas da aplicação
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/usuario-logado')
@login_required
def usuario_logado():
    return render_template('usuario-logado.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/historico')
@login_required
def historico():
    return render_template('historico.html')

@app.route('/perfil')
@login_required
def perfil():
    # Busca as informações do usuário logado
    user_response, status_code = UserController.get_user_profile()

    # Verifica se a resposta foi bem-sucedida
    if status_code != 200:
        return redirect(url_for('login'))  # Redireciona para o login se houver erro

    # Extrai os dados do usuário da resposta
    user_data = user_response.get_json()

    # Passa as informações do usuário para o template
    return render_template('perfil.html', user=user_data['user'])

@app.route('/editar-perfil')
@login_required
def editar_perfil_page():  # Renomeie a função para evitar conflito
    # Busca as informações do usuário logado
    user_response, status_code = UserController.get_user_profile()

    # Verifica se a resposta foi bem-sucedida
    if status_code != 200:
        return redirect(url_for('login'))  # Redireciona para o login se houver erro

    # Extrai os dados do usuário da resposta
    user_data = user_response.get_json()

    # Passa as informações do usuário para o template de edição
    return render_template('editar_perfil.html', user=user_data['user'])

# Rotas da API
@app.route('/api/users', methods=['POST'])
def create_user():
    return UserController.create_user()

@app.route('/api/login', methods=['POST'])
def api_login():
    return UserController.login()

@app.route('/api/agendamentos', methods=['POST'])
def agendar_servico():
    return AgendamentoController.agendar_servico()

@app.route('/api/agendamentos', methods=['GET'])
def listar_agendamentos():
    return AgendamentoController.listar_agendamentos()

@app.route('/api/agendamentos/<int:agendamento_id>', methods=['PUT'])
def editar_agendamento(agendamento_id):
    return AgendamentoController.editar_agendamento(agendamento_id)

@app.route('/api/agendamentos/<int:agendamento_id>', methods=['DELETE'])
def excluir_agendamento(agendamento_id):
    return AgendamentoController.excluir_agendamento(agendamento_id)

@app.route('/api/perfil', methods=['GET'])
@login_required
def get_perfil():
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        return jsonify({'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/perfil', methods=['PUT'])
@login_required
def api_editar_perfil():  # Renomeie a função para evitar conflito
    try:
        data = request.get_json()
        user = User.query.get(session['user_id'])

        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        # Atualiza os dados do usuário
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.bairro = data.get('bairro', user.bairro)
        user.rua = data.get('rua', user.rua)
        user.numero = data.get('numero', user.numero)
        user.cep = data.get('cep', user.cep)

        db.session.commit()

        return jsonify({'message': 'Perfil atualizado com sucesso', 'user': user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    try:
        # Remove o user_id da sessão
        session.pop('user_id', None)
        return jsonify({'message': 'Logout realizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Inicia a aplicação
if __name__ == '__main__':
    app.run(debug=True)