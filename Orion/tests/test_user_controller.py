import unittest
from flask import Flask
from config.database import db, init_db
from controllers.user_controller import UserController
from models.user import User

class TestUserController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        init_db(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        with self.app.test_request_context(json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'bairro': 'Centro',
            'rua': 'Rua Teste',
            'numero': 123,
            'cep': '12345-678' 
        }):
            response, status_code = UserController.create_user()
            print(response.get_json())  
            self.assertEqual(status_code, 201)
            self.assertIn('Usuário cadastrado com sucesso', response.get_json()['message'])

    def test_create_user_duplicate_email(self):
        # Primeiro, cria um usuário
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

        # Tenta criar outro usuário com o mesmo email
        with self.app.test_request_context(json={
            'name': 'Another User',
            'email': 'test@example.com',
            'password': 'password123',
            'bairro': 'Centro',
            'rua': 'Rua Teste',
            'numero': 123,
            'cep': '12345-678'  
        }):
            response, status_code = UserController.create_user()
            self.assertEqual(status_code, 400)
            self.assertIn('Email já cadastrado', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()