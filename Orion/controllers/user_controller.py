from flask import jsonify, request, session
from models.user import User
from config.database import db

class UserController:
    @staticmethod
    def create_user():
        try:
            data = request.get_json()

            # Verifica se o email já está cadastrado
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email já cadastrado'}), 400

            # Cria um novo usuário com os dados fornecidos
            new_user = User(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                bairro=data['bairro'],  
                rua=data['rua'],
                numero=data['numero'],        
                cep=data['cep']         
            )

            # Adiciona o novo usuário ao banco de dados
            db.session.add(new_user)
            db.session.commit()

            # Retorna uma mensagem de sucesso e os dados do usuário
            return jsonify({
                'message': 'Usuário cadastrado com sucesso',
                'user': new_user.to_dict()
            }), 201
        
        except Exception as e:
            # Em caso de erro, faz rollback e retorna uma mensagem de erro
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        

    @staticmethod
    def login():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            # Busca o usuário pelo email
            user = User.query.filter_by(email=email).first()

            # Verifica se o usuário existe e se a senha está correta
            if user and user.verify_password(password):
                session['user_id'] = user.id
                return jsonify({
                    'message': 'Login realizado com sucesso',
                    'user': user.to_dict()
                }), 200
            else:
                return jsonify({
                    'message': 'Email ou senha inválidos'
                }), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_user_profile():
        try:
            # Verifica se o usuário está logado
            if 'user_id' not in session:
                return jsonify({'error': 'Usuário não autenticado'}), 401
    
            # Busca o usuário no banco de dados
            user = User.query.get(session['user_id'])
    
            if not user:
                return jsonify({'error': 'Usuário não encontrado'}), 404
    
            # Retorna as informações do usuário
            return jsonify({
                'user': user.to_dict()
            }), 200
    
        except Exception as e:
            return jsonify({'error': str(e)}), 500