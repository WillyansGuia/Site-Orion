import unittest
from flask import Flask, session
from config.database import db, init_db
from models.user import User
from controllers.agendamento_controller import AgendamentoController
from models.agendamento import Agendamento

class TestAgendamentoControllerList(unittest.TestCase):
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

        # Cria um usuário para testar a listagem de agendamentos
        self.user = User(
            name='Test User',
            email='test@example.com',
            password='password123',
            bairro='Centro',
            rua='Rua Teste',
            numero=123,
            cep='12345-678'
        )
        db.session.add(self.user)
        db.session.commit()
        print(f"\nUsuário criado com ID: {self.user.id}")

        # Cria um agendamento para o usuário
        self.agendamento = Agendamento(
            servico='Instalação de Rede',
            data='2025-10-10',
            horario='Manhã',
            user_id=self.user.id
        )
        db.session.add(self.agendamento)
        db.session.commit()
        print(f"Agendamento criado para usuário ID: {self.agendamento.user_id}")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_listar_agendamentos(self):
        with self.app.test_request_context():
            # Configurar a sessão diretamente
            session['user_id'] = self.user.id
            print(f"Sessão configurada com user_id: {session.get('user_id')}")
            
            # Verificar a sessão antes da chamada
            print(f"Sessão antes da listagem: {dict(session)}")
            
            # Fazer a chamada para listar_agendamentos no mesmo contexto
            response, status_code = AgendamentoController.listar_agendamentos()
            
            print(f"Status code retornado: {status_code}")
            print(f"Resposta completa: {response.get_json()}")
            print(f"Sessão após a listagem: {dict(session)}")
            
            # Verificações
            self.assertEqual(status_code, 200)
            response_data = response.get_json()
            self.assertIn('agendamentos', response_data)
            self.assertEqual(len(response_data['agendamentos']), 1)
            
            # Verificar os dados do agendamento
            agendamento = response_data['agendamentos'][0]
            self.assertEqual(agendamento['servico'], 'Instalação de Rede')
            self.assertEqual(agendamento['horario'], 'Manhã')

    def test_listar_agendamentos_unauthenticated(self):
        with self.app.test_request_context():
            # Não configuramos a sessão neste teste
            response, status_code = AgendamentoController.listar_agendamentos()
            print(f"\nTeste não autenticado - Status code: {status_code}")
            print(f"Teste não autenticado - Resposta: {response.get_json()}")
            self.assertEqual(status_code, 401)
            self.assertIn('Usuário não autenticado', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()