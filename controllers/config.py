import os
basedir = os.path.abspath(os.path.dirname(__file__))


def init_app(app):

    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY'] = '5AF1F6861BDB64220BD054FDEECEC5EB1F65CA2B741D719808E90A5F0BACF705'
    app.config['ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.config['ROOT_DIR'], '..', 'static', 'img')
    app.config['DATABASE_FILE'] = 'BDGestao.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(app.config['ROOT_DIR'], '..',
                     'models', app.config['DATABASE_FILE'])
    app.config['SQLALCHEMY_ECHO'] = False

    if app.config['ENV'] == 'development':
        
        app.config['DEBUG'] = True
        app.config['FLASK_ADMIN_SWATCH'] = 'flatly'  # united flatly cerulean
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    elif app.config['ENV'] == 'production':
        app.config['DEBUG'] = False
        app.config['FLASK_ADMIN_SWATCH'] = 'united'  # united flatly cerulean
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = False
        app.config['DEBUG_TB_PROFILER_ENABLED'] = False
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
