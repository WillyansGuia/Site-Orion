from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    user = os.getenv('DB_USER', 'root')
    password = quote_plus(os.getenv('DB_PASSWORD', '123456'))
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '3306')
    database = os.getenv('DB_NAME', 'orion_db')
    
    # Usando MySQL
    DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)