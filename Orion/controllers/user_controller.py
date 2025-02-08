from flask import jsonify, request, session
from models.user import User
from config.database import db


class UserController:
    @staticmethod
    def create_user():
        try:
            data = request.get_json()

            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email já cadastrado'}), 400


            new_user = User (
                name=data['name'],
                email=data['email'],
                password=data['password']
            )

            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                'message': 'Usuário cadastrado com sucesso',
                'user': new_user.to_dict()
            }), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}),500
        

    @staticmethod
    def login():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')


            user = User.query.filter_by(email=email).first()


            if user and user.verify_password(password):
                session['user_id'] = user.id
                return jsonify({
                    'message': 'Login realizado com sucesso',
                    'user': user.to_dict()
                }),200
            else:
                return jsonify({
                    'message': 'Email ou senha inválidos'
                }), 401
        except Exception as e:
            return jsonify({'error': str(e)}),500