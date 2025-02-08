from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)  
    rua = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    cep = db.Column(db.String(10), nullable=False)      

    def __init__(self, name, email, password, bairro, rua, numero, cep):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.bairro = bairro  
        self.rua = rua
        self.numero = numero        
        self.cep = cep        

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bairro': self.bairro,  
            'rua': self.rua, 
            'numero': self.numero,       
            'cep': self.cep         
        }