import os
from flask import render_template, request,  session, redirect, flash, current_app, url_for
from flask import send_from_directory, stream_with_context, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime, date
from controllers.db import db
from controllers.manager import login_manager
from models.tables import User, Conta, Despesa, Tipo, Categoria
from flask_login import login_user, logout_user, current_user
import secrets


ALGORITMO = "pbkdf2:sha256"

EXTENSOES_PERMITIDAS = {"png", "bmp", "jpg", "jpe", "jpeg", "gif"}


dta = date.today().strftime("%d-%m-%Y")
d, m, y = dta.split('-')
data_inicial = date(int(2022), int(1), int(1))
data_final = date(int(y), int(m), int(d))


def init_app(app):

    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1] in EXTENSOES_PERMITIDAS

    # ---ROTAS---------------------------------------------------------------
    @app.route('/')
    def index():
        return "Este é um teste"
    
    @app.route('/inicio', methods=['GET', 'POST'])
    def inicio():
        if request.method == 'POST':
            email = request.form.get('usuario')
            pwd = request.form.get('password')
            user = User.query.filter(
                (User.username == email) | (User.email == email)).first()
            if not user or not user.verify_password(pwd):
                return redirect(url_for('inicio'))
            else:
                login_user(user)
                return redirect(url_for('inicio'))
        return render_template('inicio.html')

    # ----------------------------------------------------------------------
    @app.route('/logout')
    def logout():
        logout_user()
        #  flash(f'Usuario saiu', 'success')
        return redirect(url_for('inicio'))

    # ----------------------------------------------------------------------
    @app.route('/lista',  methods=['GET', 'POST'])
    def lista():

        LOGADO = current_user.id
        contas = Conta.query.filter(Conta.usua_id == LOGADO).all()
        return render_template('lista.html', contas=contas,  titulo='Listagem das Contas', data_inicial=data_inicial, data_final=data_final)

    # ----------------------------------------------------------------------
    @app.route('/grafico1',  methods=['GET', 'POST'])
    def grafico1():
        contas = Conta.query.all()
        tipo = Categoria.query.all()
        dic = {'Task': ' Hora e Dia'}

        x = -1
        for a in tipo:
            x = x+1
            z = -1
            vlr = float(0)
            for b in contas:
                if tipo[x].name == contas[z].categoria and contas[z].operacao == 'RECEITA':
                    vlr = vlr + float(contas[z].saldo)
                z = z+1
            dic['RECEITA ' + tipo[x].name] = int(vlr)

        x = -1
        for a in tipo:
            x = x+1
            z = -1
            vlr = float(0)
            for b in contas:
                if tipo[x].name == contas[z].categoria and contas[z].operacao == 'DESPESA':
                    vlr = vlr + float(contas[z].saldo)
                z = z+1
            dic['DESPESA ' + tipo[x].name] = int(vlr)

        return render_template('grafico1.html',   titulo='RECEITAS  X  DESPESAS', dados=dic, data_inicial=data_inicial, data_final=data_final)

    # ----------------------------------------------------------------------
    @app.route('/grafico2',  methods=['GET', 'POST'])
    def grafico2():
        contas = Conta.query.filter(Conta.operacao == 'DESPESA').all()
        tipo = Tipo.query.all()

        dic = {'Task': ' Hora e Dia'}
        x = -1
        for a in tipo:
            x = x+1
            z = -1
            vlr = float(0)
            for b in contas:
                if tipo[x].name == contas[z].tipo:
                    vlr = vlr + float(contas[z].saldo)
                z = z+1
            dic[tipo[x].name] = int(vlr)

        return render_template('grafico2.html',   titulo='TIPOS DE DESPESAS', data=dic, data_inicial=data_inicial, data_final=data_final)

    # ----------------------------------------------------------------------
    @app.route('/grafico3',  methods=['GET', 'POST'])
    def grafico3():
        contas = Conta.query.filter(Conta.operacao == 'DESPESA').all()
        tipo = Categoria.query.all()
        dic = {'Task': ' Hora e Dia'}
        x = -1
        for a in tipo:
            x = x+1
            z = -1
            vlr = float(0)
            for b in contas:
                if tipo[x].name == contas[z].categoria:
                    vlr = vlr + float(contas[z].saldo)
                z = z+1
            dic[tipo[x].name] = int(vlr)

        return render_template('grafico3.html',   titulo='CATEGORIAS  DE  DESPESAS', data=dic, data_inicial=data_inicial, data_final=data_final)
     # ----------------------------------------------------------------------

    @app.route('/listamov/<int:id>')
    def listamov(id):
        contas = Conta.query.filter(Conta.id == id).all()
        despesas = Despesa.query.filter(Despesa.cta_id == id).all()
        oper = contas[0].operacao
        categ = contas[0].categoria
        tpo = contas[0].tipo
        cta = contas[0].conta
        cta_id = id
        return render_template('listamov.html', despesas=despesas, conta=oper + ' ' + tpo + ' - ' + categ + ' - ' + cta, cta_id=cta_id, titulo='Movimentos Lançados', data_inicial=data_inicial, data_final=data_final)

     # ----------------------------------------------------------------------
    @app.route('/addconta', methods=['GET', 'POST'])
    def addconta():
        LOGADO = current_user.id
        vtipo = Tipo.query.all()
        vcateroria = Categoria.query.all()
        titulo = 'Cadastro de Contas'

        if request.method == 'POST':
            usua_id = LOGADO
            contas = request.form.get('xconta')
            operacao = request.form.get('xoperacao')
            tipos = request.form.get('xtipo')
            categorias = request.form.get('xcategoria')
            saldos = 0
            testa = Conta.query.filter(Conta.conta == contas).all()

            if testa:
                flash(f'Conta ja existe', 'danger')
                return redirect(url_for('addconta'))
            else:
                if contas and usua_id and tipos and categorias:
                    sql = Conta(conta=contas,  usua_id=usua_id,
                                saldo=saldos, tipo=tipos,  operacao=operacao, categoria=categorias)
                    db.session.add(sql)
                    db.session.commit()
                    flash(f'A conta salva com sucesso', 'success')
                    return redirect(url_for('addconta'))
                else:
                    flash(f'Dados incompletos', 'danger')
                    return redirect(url_for('addconta'))
        return render_template('addconta.html', tipos=vtipo, categorias=vcateroria, titulo=titulo, data_inicial=data_inicial, data_final=data_final)

    # ----------------------------------------------------------------------
    @app.route('/adduser', methods=['GET', 'POST'])
    def adduser():

        if request.method == 'POST':
            username = request.form.get('username')
            name = request.form.get('name')
            email = request.form.get('email')
            pwd = request.form.get('password')
            admin = False
            file = request.files['minhaimage']
            savePath = os.path.join(
                app.config["UPLOAD_FOLDER"], secure_filename(file.filename))

            if current_user.is_authenticated:
                flash(f' Usuario ja  autenticado', 'danger')
                return redirect(url_for('adduser'))

            user = User.query.filter(
                (User.username == email) | (User.email == email)).first()
            if user:
                flash(f' Usuario ja cadastrado ', 'danger')
                return redirect(url_for('adduser'))

            print(name)

            print(savePath)

            if username and name and email and pwd and admin != '':
                image_sn = allowed_file(file.filename)
                print(username)
                print(image_sn)
                if image_sn == True:
                    file.save(savePath)
                    imagem = str(file.filename)
                else:
                    imagem = 'logo.jpg'

                print(imagem)

                user = User(username=username,  name=name, email=email,
                            password=pwd,  admin=admin, imagem=imagem)
                db.session.add(user)
                db.session.commit()

                user = User.query.filter(
                    (User.username == email) | (User.email == email)).first()

                login_user(user)
                id = current_user.id

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

                # ----------------------------------------------------------------------------------

                flash(f'Usuario {username} salvo com sucesso', 'success')
                return redirect(url_for('adduser'))
            else:
                flash(f'ERRO -  Dados incompletos', 'danger')
                return redirect(url_for('adduser'))

        return render_template('adduser.html', titulo='Cadastro de usuario', data_inicial=data_inicial, data_final=data_final)

    # ----------------------------------------------------------------------
    @app.route('/addMovDesp',  methods=['GET', 'POST'])
    def addMovDesp():
        LOGADO = int(current_user.id)
        contas = Conta.query.filter(
            (Conta.operacao == 'DESPESA') & (Conta.usua_id == LOGADO)).all()
        titulo = 'Lançamento     de     Despesas'
        data_atual = date.today().strftime("%d-%m-%Y")
        d, m, y = data_atual.split('-')
        data_atual = date(int(y), int(m), int(d))
        if request.method == 'POST':
            usua_id = LOGADO
            cta_id = request.form.get('idConta')
            dt = request.form.get('xdata')
            descricao = request.form.get('xdescricao')
            valor = request.form.get('xvalor')

            if usua_id and cta_id and dt and descricao and valor:
                valor = float(valor)
                conta_id = int(cta_id)
                y, m, d = dt.split('-')
                dta = datetime(int(y), int(m), int(d))
                despesas = Despesa(usua_id=usua_id, cta_id=conta_id,
                                   dta=dta, descricao=descricao, valor=valor)
                db.session.add(despesas)
                # --------Atualiza Saldo das contas ---------------
                sql = Conta.query.get_or_404(conta_id)
                anterior = float(sql.saldo)
                sql.saldo = anterior + valor
                # --------------------------------- ---------------
                db.session.commit()
                flash(f'SUCESSO  -  Lançamento salvo', 'success')
            else:
                flash(f'ERRO - Dados incompletos', 'danger')
                return redirect(url_for('addMovDesp'))
        return render_template('addMovDesp.html', contas=contas,  titulo=titulo, data_atual=data_atual, data_inicial=data_inicial, data_final=data_final)

 # ----------------------------------------------------------------------
    @app.route('/addMovRec',  methods=['GET', 'POST'])
    def addMovRec():

        LOGADO = int(current_user.id)
        contas = Conta.query.filter(
            (Conta.operacao == 'RECEITA') & (Conta.usua_id == LOGADO)).all()
        titulo = 'Lançamento de Receitas'
        data_atual = date.today().strftime("%d-%m-%Y")
        d, m, y = data_atual.split('-')
        data_atual = date(int(y), int(m), int(d))
        if request.method == 'POST':
            usua_id = LOGADO
            cta_id = request.form.get('idConta')
            dt = request.form.get('xdata')
            descricao = request.form.get('xdescricao')
            valor = request.form.get('xvalor')

            if usua_id and cta_id and dt and descricao and valor:
                valor = float(valor)
                conta_id = int(cta_id)
                y, m, d = dt.split('-')
                dta = datetime(int(y), int(m), int(d))
                despesas = Despesa(usua_id=usua_id, cta_id=conta_id,
                                   dta=dta, descricao=descricao, valor=valor)
                db.session.add(despesas)
                # --------Atualiza Saldo das contas ---------------
                sql = Conta.query.get_or_404(conta_id)
                anterior = float(sql.saldo)
                sql.saldo = anterior + valor
                # --------------------------------- ---------------
                db.session.commit()
                flash(f'SUCESSO  -  Lançamento salvo', 'success')
            else:
                flash(f'ERRO - Dados incompletos', 'danger')
                return redirect(url_for('addMovRec'))
        return render_template('addMovRec.html', contas=contas,  titulo=titulo, data_atual=data_atual, data_inicial=data_inicial, data_final=data_final)

 # ----------------------------------------------------------------------
    @app.route('/atualiza')
    def atualiza():
        #LOGADO = int(current_user.id)
        despesas = Despesa.query.all()
        contas = Conta.query.all()
        x = -1
        for a in contas:
            x = x+1
            cont_user = contas[x].usua_id
            cont_id = contas[x].id
            z = -1
            v1 = float(0)
            for b in despesas:
                z = z + 1
                desp_user = int(despesas[z].usua_id)
                desp_id = int(despesas[z].cta_id)
                if (cont_user == desp_user) & (cont_id == desp_id):
                    v1 = v1 + float(despesas[z].valor)
            saldo_atual = Conta.query.get_or_404(cont_id)
            saldo_atual.saldo = v1
            db.session.commit()
        return redirect(url_for('lista'))

 # ----------------------------------------------------------------------
    @app.route('/deleteMov/<int:id>', methods=['GET', 'POST'])
    def deleteMov(id):
        despesas = Despesa.query.get_or_404(id)
        id_conta = despesas.cta_id
        valor = float(despesas.valor)
        if request.method == "POST":
            db.session.delete(despesas)

            sql = Conta.query.get_or_404(id_conta)
            anterior = float(sql.saldo)
            sql.saldo = anterior - valor
            db.session.commit()
            flash(
                f'O registro {despesas.id} foi excluido', 'success')
            return redirect(url_for('listamov', id=id_conta))

        return redirect(url_for('listamov', id=id_conta))
