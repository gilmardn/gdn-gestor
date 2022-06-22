
from flask_admin.contrib.sqla import ModelView
from controllers.db import db
from models.tables import User, Conta, Despesa, Tipo, Categoria
from controllers.admin import admin


def init_app(app):
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(DespesaAdmin(Conta, db.session))
    admin.add_view(DespesaAdmin(Despesa, db.session))
    admin.add_view(DespesaAdmin(Tipo, db.session))
    admin.add_view(DespesaAdmin(Categoria, db.session))


def formatar_usuario(self, request, user, *args):
    return user.email.split('@')[0]  # Elimina texto apos o '@'


class UserAdmin(ModelView):
    column_formatters = {"email": formatar_usuario}  # Função Formata coluna
    column_list = ['email', 'passwd', 'admin']  # Colunas a ser exibida
    column_searchable_list = ['email']  # Habilita a coluna para consulta
    column_filters = ['email', 'admin']  # Habilita filtro
    can_edit = True  # Habilita ou desabilita as funçoe abaixo
    can_create = True  # Habilita ou desabilita as funçoe abaixo
    can_delete = True  # Habilita ou desabilita as funçoe abaixo


class TipoAdmin(ModelView):
    '''Interface admin de category'''
    column_list = ['id', 'tipo', 'user_id']  # Colunas a ser exibida


class DespesaAdmin(ModelView):
    '''Interface admin de category'''
