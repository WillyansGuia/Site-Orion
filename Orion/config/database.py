from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    user = os.getenv('DB_USER', 'postgres')
    password = quote_plus(os.getenv('DB_PASSWORD'))
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME', 'orion_db')
    
    DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from flask_migrate import upgrade
        upgrade()