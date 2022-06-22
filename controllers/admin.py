from flask_admin import Admin


admin = Admin(name="Gestão Foods", template_mode="bootstrap4")


def init_app(app):
    admin.init_app(app)



   






