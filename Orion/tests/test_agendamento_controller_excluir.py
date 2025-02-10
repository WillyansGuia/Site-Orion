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

    def test_excluir_agendamento_sucesso(self):
        with self.app.test_request_context():
            # Configurar a sessão com o usuário correto
            session['user_id'] = self.user1.id
            print(f"\nSessão configurada com user_id: {session.get('user_id')}")
            print(f"Tentando excluir agendamento ID: {self.agendamento.id}")
            
            response, status_code = AgendamentoController.excluir_agendamento(self.agendamento.id)
            print(f"Status code retornado: {status_code}")
            print(f"Resposta completa: {response.get_json()}")
            
            self.assertEqual(status_code, 200)
            self.assertIn('Agendamento excluído com sucesso', response.get_json()['message'])
            self.assertIsNone(Agendamento.query.get(self.agendamento.id))

    def test_excluir_agendamento_unauthenticated(self):
        with self.app.test_request_context():
            print(f"\nTentando excluir agendamento sem autenticação")
            response, status_code = AgendamentoController.excluir_agendamento(self.agendamento.id)
            
            print(f"Status code retornado: {status_code}")
            print(f"Resposta completa: {response.get_json()}")
            
            self.assertEqual(status_code, 401)
            self.assertIn('Usuário não autenticado', response.get_json()['error'])
            self.assertIsNotNone(Agendamento.query.get(self.agendamento.id))

    def test_excluir_agendamento_outro_usuario(self):
        with self.app.test_request_context():
            # Configurar a sessão com outro usuário
            session['user_id'] = self.user2.id
            print(f"\nTentando excluir agendamento de outro usuário")
            
            response, status_code = AgendamentoController.excluir_agendamento(self.agendamento.id)
            print(f"Status code retornado: {status_code}")
            print(f"Resposta completa: {response.get_json()}")
            
            self.assertEqual(status_code, 403)
            self.assertIn('Você não tem permissão', response.get_json()['error'])
            self.assertIsNotNone(Agendamento.query.get(self.agendamento.id))

    def test_excluir_agendamento_inexistente(self):
        with self.app.test_request_context():
            session['user_id'] = self.user1.id
            print(f"\nTentando excluir agendamento inexistente")
            
            response, status_code = AgendamentoController.excluir_agendamento(9999)
            print(f"Status code retornado: {status_code}")
            print(f"Resposta completa: {response.get_json()}")
            
            self.assertEqual(status_code, 404)
            self.assertIn('Agendamento não encontrado', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()