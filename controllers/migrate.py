from flask_migrate import Migrate
from controllers.db import db
from models import tables

migrate = Migrate()

def init_app(app):
    migrate.init_app(app, db)

#   set FLASK_APP=app.py
#   flask db init
#   flask db migrate -m "Alterar relacionamentos"