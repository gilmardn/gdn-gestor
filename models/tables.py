# -*- encoding: utf-8 -*-

from datetime import datetime
from controllers.db import db
from controllers.manager import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# -----------  usuario Logado  --------------------------------------


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):  # Usuario
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), unique=True)
    password = db.Column(db.String(240), nullable=False)
    name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(200), unique=True)
    imagem = db.Column(db.String(240), unique=False,
                       nullable=False, default='logo.jpg')
    admin = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, username, password, name, email, imagem, admin):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email
        self.imagem = imagem
        self.admin = admin

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return '<User %>' % self.username


# ----------------------------------------------------------------------
class Conta(db.Model):  # Alimentação   casa  vestuario
    __tablename__ = "contas"
    id = db.Column(db.Integer, primary_key=True)
    conta = db.Column(db.String(40), unique=False)
    usua_id = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(40), unique=False)
    categoria = db.Column(db.String(40), unique=False)
    operacao = db.Column(db.String(10), unique=False, default='DESPESA')
    saldo = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    def __init__(self, conta, usua_id, tipo, categoria, operacao, saldo):
        self.conta = conta
        self.usua_id = usua_id
        self.tipo = tipo
        self.categoria = categoria
        self.operacao = operacao
        self.saldo = saldo

    def __repr__(self):
        return '<Contas %r>' % self.conta


# ----------------------------------------------------------------------
class Despesa(db.Model):
    __tablename__ = "despesas"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(80), nullable=False)
    usua_id = db.Column(db.Integer, nullable=False)
    cta_id = db.Column(db.Integer, nullable=False)
    dta = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor = db.Column(db.Numeric(10, 2), nullable=False)

    def __init__(self, descricao, usua_id, cta_id, dta, valor):
        self.descricao = descricao
        self.usua_id = usua_id
        self.cta_id = cta_id
        self.dta = dta
        self.valor = valor

    def __repr__(self):
        return '<Despesas %r>' % self.descricao


class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Categorias %r>' % self.name


class Tipo(db.Model):
    __tablename__ = "tipos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Tipos %r>' % self.name
