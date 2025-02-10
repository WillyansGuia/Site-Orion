import unittest
from flask import Flask, session
from config.database import db, init_db
from models.user import User
from controllers.agendamento_controller import AgendamentoController

class TestAgendamentoController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.secret_key = 'chave-desenvolvimento'
        init_db(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Verifica se o usuário já existe antes de criar
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            # Cria um usuário para testar o agendamento
            user = User(
                name='Test User',
                email='test@example.com',
                password='password123',
                bairro='Centro',
                rua='Rua Teste',
                numero=123,
                cep='12345-678'
            )
            db.session.add(user)
            db.session.commit()

        # Simula o login do usuário
        with self.app.test_request_context():
            session['user_id'] = user.id
            print("Sessão no setUp:", session)  # Depuração: Verifique a sessão

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_agendar_servico(self):
        with self.app.test_request_context(json={
            'servico': 'Instalação de Rede',
            'data': '2025-10-10',
            'horario': 'Manhã'
        }):
            # Força a sessão a ser a mesma do setUp
            session['user_id'] = 1  # Ou use a variável user.id
            print("Sessão antes do agendamento:", session)  # Depuração: Verifique a sessão
            response, status_code = AgendamentoController.agendar_servico()
            print("Resposta do agendamento:", response.get_json())  # Depuração: Verifique a resposta
            self.assertEqual(status_code, 201)
            self.assertIn('Agendamento realizado com sucesso', response.get_json()['message'])

    def test_agendar_servico_unauthenticated(self):
        # Remove o user_id da sessão para simular um usuário não autenticado
        with self.app.test_request_context():
            session.pop('user_id', None)

        with self.app.test_request_context(json={
            'servico': 'Instalação de Rede',
            'data': '2025-10-10',
            'horario': 'Manhã'
        }):
            response, status_code = AgendamentoController.agendar_servico()
            self.assertEqual(status_code, 401)
            self.assertIn('Usuário não autenticado', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()