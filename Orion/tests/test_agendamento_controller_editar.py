import unittest
from flask import Flask, session
from config.database import db, init_db
from models.user import User
from controllers.agendamento_controller import AgendamentoController
from models.agendamento import Agendamento

class TestAgendamentoControllerDelete(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.app.secret_key = 'chave-desenvolvimento'        
        init_db(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        db.create_all()

        # Cria dois usuários para testar diferentes cenários
        self.user1 = User(
            name='Test User 1',
            email='test1@example.com',
            password='password123',
            bairro='Centro',
            rua='Rua Teste',
            numero=123,
            cep='12345-678'
        )
        db.session.add(self.user1)
        
        self.user2 = User(
            name='Test User 2',
            email='test2@example.com',
            password='password123',
            bairro='Centro',
            rua='Rua Teste',
            numero=124,
            cep='12345-678'
        )
        db.session.add(self.user2)
        db.session.commit()
        print(f"\nUsuários criados com IDs: {self.user1.id} e {self.user2.id}")

        # Cria um agendamento para o usuário 1
        self.agendamento = Agendamento(
            servico='Instalação de Rede',
            data='2025-10-10',
            horario='Manhã',
            user_id=self.user1.id
        )
        db.session.add(self.agendamento)
        db.session.commit()
        print(f"Agendamento criado com ID: {self.agendamento.id} para usuário ID: {self.agendamento.user_id}")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_editar_agendamento(self):
        agendamento = Agendamento.query.first()
        with self.app.test_request_context(json={
            'servico': 'Sistemas de Segurança',
            'data': '2025-10-11',
            'horario': 'Tarde'
        }):
            # Força a sessão a ser a mesma do setUp
            session['user_id'] = self.user1.id
            print("Sessão antes da edição:", session)  # Depuração: Verifique a sessão
            response, status_code = AgendamentoController.editar_agendamento(agendamento.id)
            print("Resposta da edição:", response.get_json())  # Depuração: Verifique a resposta
            self.assertEqual(status_code, 200)
            self.assertIn('Agendamento atualizado com sucesso', response.get_json()['message'])

    def test_editar_agendamento_unauthenticated(self):
        agendamento = Agendamento.query.first()
        # Remove o user_id da sessão para simular um usuário não autenticado
        with self.app.test_request_context():
            session.pop('user_id', None)
    
        with self.app.test_request_context(json={
            'servico': 'Sistemas de Segurança',
            'data': '2025-10-11',
            'horario': 'Tarde'
        }):
            response, status_code = AgendamentoController.editar_agendamento(agendamento.id)
            print("Resposta da edição (não autenticado):", response.get_json())  # Depuração: Verifique a resposta
            self.assertEqual(status_code, 401)  # Espera-se 401 (não autenticado)
            self.assertIn('Usuário não autenticado', response.get_json()['error'])
if __name__ == '__main__':
    unittest.main()