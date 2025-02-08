from config.database import db

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.Integer, primary_key=True)
    servico = db.Column(db.String(100), nullable=False)  
    data = db.Column(db.Date, nullable=False)            
    horario = db.Column(db.String(50), nullable=False)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  

    def __init__(self, servico, data, horario, user_id):
        self.servico = servico
        self.data = data
        self.horario = horario
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'servico': self.servico,
            'data': self.data.isoformat(),  
            'horario': self.horario,
            'user_id': self.user_id
        }