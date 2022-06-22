import click
from controllers.db import db
from models.tables import User, Conta, Categoria, Tipo


def init_app(app):

    @app.cli.command()
    def create_db():
        #   .venv\scripts\activate
        #   Botar APP nas mesma pasta do RUN
        #   flask create-db
        # ------   e o primeiro Usuario---------------
        db.create_all()

        user = User(username="admin", password="admin",
                    name='Administrador', email="administrador@admin.com.br", imagem='logo.jpg', admin=True)
        db.session.add(user)
        db.session.commit()
        # ----------------------------------------------------------------------------------

        categoria = Categoria(name="FIXAS")
        db.session.add(categoria)
        categoria = Categoria(name="VARIAVEIS")
        db.session.add(categoria)
        categoria = Categoria(name="EXTRAS")
        db.session.add(categoria)
        db.session.commit()
        # ----------------------------------------------------------------------------------
        tipo = Tipo(name="ALIMENTAÇÃO")
        db.session.add(tipo)
        tipo = Tipo(name="ALUGUEL")
        db.session.add(tipo)
        tipo = Tipo(name="JUROS")
        db.session.add(tipo)
        tipo = Tipo(name="MORADIA")
        db.session.add(tipo)
        tipo = Tipo(name="SAUDE")
        db.session.add(tipo)
        tipo = Tipo(name="VEICULO")
        db.session.add(tipo)
        tipo = Tipo(name="EDUCAÇÃO")
        db.session.add(tipo)
        tipo = Tipo(name="IMPOSTOS")
        db.session.add(tipo)
        tipo = Tipo(name="LAZER")
        db.session.add(tipo)
        tipo = Tipo(name="SALARIO")
        db.session.add(tipo)
        tipo = Tipo(name="DIVERSOS")
        db.session.add(tipo)
        db.session.commit()
        # ----------------------------------------------------------------------------------

        id = 1
        conta = Conta(conta='Salario',            usua_id=id,
                      categoria='FIXAS',     tipo='SALARIOS',     operacao='RECEITA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Outras Receitas',    usua_id=id,
                      categoria='VARIAVEIS', tipo='JUROS',     operacao='RECEITA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Mercado',            usua_id=id,
                      categoria='FIXAS',     tipo='ALIMENTAÇÃO',  operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Farmacia',           usua_id=id,
                      categoria='VARIAVEIS', tipo='SAUDE',        operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Plano de Saude',     usua_id=id,
                      categoria='FIXAS',     tipo='SAUDE',        operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Energia Eletria',    usua_id=id,
                      categoria='FIXAS',     tipo='MORADIA',      operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Agua e Saneamento',  usua_id=id,
                      categoria='FIXAS',     tipo='MORADIA',      operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Internet e TV',      usua_id=id,
                      categoria='FIXAS',     tipo='LAZER',      operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Cursos',             usua_id=id,
                      categoria='VARIAVEIS', tipo='EDUCAÇÃO',     operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Ipva/Iptu',          usua_id=id,
                      categoria='FIXAS',     tipo='IMPOSTOS',     operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='IRPF',               usua_id=id,
                      categoria='FIXAS',     tipo='IMPOSTOS',     operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Prestação Carro',    usua_id=id,
                      categoria='VARIAVEIS', tipo='VEICULO',      operacao='DESPESA', saldo=0)
        db.session.add(conta)
        conta = Conta(conta='Viagens',            usua_id=id,
                      categoria='EXTRAS',    tipo='LAZER',        operacao='DESPESA', saldo=0)
        db.session.add(conta)
        db.session.commit()

# ----------------------------------------------------------------------

    @app.cli.command()
    @click.option("--email", "-e")
    @click.option("--password", "-p")
    @click.option("--admin", "-a", is_flag=True, default=False)
    def add_user(email, password, admin):
        #   flask add_user
        '''  adiciona Usuario'''
        user = User(email=email, password=password, admin=admin)
        db.session.add(user)
        db.session.commit()
        click.echo("===========================================================")
        click.echo(f"==   Usuarios {email} criado com sucesso    ==")
        click.echo("===========================================================")

    @app.cli.command()
    def listar_pedidos():
        ''' Este comando Lista Pedido '''
        return "Lista pedidos"

    @app.cli.command()
    def listar_usuarios():
        ''' Este comando Lista Usuarios '''
        users = User.query.all()
        click.echo("===========================================================")
        click.echo(f"Lista de Usuarios { users } ")
        click.echo("===========================================================")
