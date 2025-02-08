from flask import Flask, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_migrate import Migrate
from config.database import init_db, db
from controllers.user_controller import UserController
from controllers.agendamento_controller import AgendamentoController
from functools import wraps

app = Flask(__name__)
CORS(app)

init_db(app)

migrate = Migrate(app, db)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return decorated_function

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
def historico():
    return render_template('historico.html')

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
app.secret_key = 'chave-desenvolvimento'

if __name__ == '__main__':
    app.run(debug=True)

