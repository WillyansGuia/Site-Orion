from flask import jsonify, request, session
from models.agendamento import Agendamento
from config.database import db
from datetime import datetime

class AgendamentoController:
    @staticmethod
    def agendar_servico():
        try:
            data = request.get_json()

            # Verifica se o usuário está logado
            if 'user_id' not in session:
                return jsonify({'error': 'Usuário não autenticado'}), 401

            # Converte a data do formato string para o tipo Date
            data_agendamento = datetime.strptime(data['data'], '%Y-%m-%d').date()

            # Cria um novo agendamento
            novo_agendamento = Agendamento(
                servico=data['servico'],
                data=data_agendamento,
                horario=data['horario'],
                user_id=session['user_id']  
            )

            # Adiciona o agendamento ao banco de dados
            db.session.add(novo_agendamento)
            db.session.commit()

            return jsonify({
                'message': 'Agendamento realizado com sucesso',
                'agendamento': novo_agendamento.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def listar_agendamentos():
        try:
            if 'user_id' not in session:
                return jsonify({'error': 'Usuário não autenticado'}), 401

            agendamentos = Agendamento.query.filter_by(user_id=session['user_id']).all()
            return jsonify({
                'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def editar_agendamento(agendamento_id):
        try:
            data = request.get_json()
    
            # Busca o agendamento pelo ID
            agendamento = Agendamento.query.get(agendamento_id)
            if not agendamento:
                return jsonify({'error': 'Agendamento não encontrado'}), 404
    
            # Verifica se o agendamento pertence ao usuário logado
            if agendamento.user_id != session['user_id']:
                return jsonify({'error': 'Você não tem permissão para editar este agendamento'}), 403
    
            # Atualiza os dados do agendamento
            agendamento.servico = data['servico']
            agendamento.data = datetime.strptime(data['data'], '%Y-%m-%d').date()
            agendamento.horario = data['horario']
    
            db.session.commit()
            return jsonify({
                'message': 'Agendamento atualizado com sucesso',
                'agendamento': agendamento.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def excluir_agendamento(agendamento_id):
        try:
            agendamento = Agendamento.query.get(agendamento_id)
            if not agendamento:
                return jsonify({'error': 'Agendamento não encontrado'}), 404

            db.session.delete(agendamento)
            db.session.commit()
            return jsonify({'message': 'Agendamento excluído com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500