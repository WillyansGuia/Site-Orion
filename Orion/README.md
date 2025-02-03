# Projeto Web Flask

## Pré-requisitos
- Python 3.8+
- PostgreSQL

## Instalação

1. Clone e acesse o projeto
```bash
git https://github.com/WillyansGuia/Site-Orion.git
cd Orion
```

2. Configure o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure o .env na raiz
```
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orion_db
FLASK_SECRET_KEY=f590c6993b8947abee9fc82927e85d81
```

5. Configure as migrations e inicie o banco
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Execute o projeto
```bash
python app.py
```

## Estrutura
```
projeto/
├── app.py
├── config/
│   └── database.py
├── controllers/
│   └── user_controller.py
├── models/
│   └── user.py
├── templates/
├── static/
└── requirements.txt
```

## Comandos Úteis
- Atualizar dependências: `pip install -r requirements.txt`
- Nova migration: `flask db migrate -m "Descrição"`
- Aplicar migrations: `flask db upgrade`