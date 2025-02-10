import unittest
from flask import Flask
from config.database import db, init_db
from controllers.user_controller import UserController
from models.user import User


class TestUserControllerLogin(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.secret_key = 'chave-desenvolvimento'
        init_db(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Cria um usuário para testar o login
        user = User(
            name='Test User',
            email='test@example.com',
            password='password123',  # A senha será hasheada no modelo
            bairro='Centro',
            rua='Rua Teste',
            numero=123,
            cep='12345-678'
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_success(self):
        with self.app.test_request_context(json={
            'email': 'test@example.com',
            'password': 'password123'
        }):
            response, status_code = UserController.login()
            print(response.get_json())  # Depuração: Verifique a resposta
            self.assertEqual(status_code, 200)
            self.assertIn('Login realizado com sucesso', response.get_json()['message'])

    def test_login_failure(self):
        with self.app.test_request_context(json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }):
            response, status_code = UserController.login()
            self.assertEqual(status_code, 401)
            self.assertIn('Email ou senha inválidos', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()