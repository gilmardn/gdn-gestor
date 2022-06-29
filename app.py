import os
from flask import Flask
from controllers import config
from controllers import rotas
from controllers.db import db
from controllers.admin import admin
from controllers import cli
from controllers import toolbar
from controllers import migrate
from controllers import adm
from controllers import manager


def create_app():
    app = Flask(__name__, template_folder='templates')

    config.init_app(app)
    rotas.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    cli.init_app(app)
    adm.init_app(app)
    manager.init_app(app)

    return app


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_APP'] = 'app.py'
    #os.environ['FLASK_ENV'] = 'production'
    app = create_app()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


#   https://www.youtube.com/watch?v=vRgay-IXeek
