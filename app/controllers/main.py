#!/usr/bin/python
# coding=utf-8
# -------------------------------------------------------------
#       LB2 Mail Migration
#
#       Autor: Tiago M Reichert
#       Data Inicio:  20/04/2017
#       Data Release:
#       email: tiago.miguel@lb2.com.br
#       Versão: v1.0a
#       LB2 Consultoria - Leading Business 2 the Next Level!
# --------------------------------------------------------------

from flask import render_template, request, Blueprint, redirect, url_for, flash, make_response
from app.models import db, Message, Account, Server, Status, Company, Migration
from datetime import datetime
from app.utils import authentication

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('Index.html')


@main.route('/create_client', methods=['GET', 'POST'])
@authentication.admin.login_required
def create_client():
    if request.method == 'GET':
        return render_template('CreateClient.html')
    elif request.method == 'POST':
        c = Company(name=request.form['name'], contact_number=request.form['contact_number'], contact_name=request.form['contact_name'], cnpj=request.form['cnpj'])
        db.session.add(c)
        db.session.commit()
        return render_template('Index.html')


@main.route('/create_server', methods=['GET', 'POST'])
@authentication.admin.login_required
def create_server():
    if request.method == 'GET':
        return render_template('CreateServer.html')
    elif request.method == 'POST':
        if request.form.get('ssl'):
            s = Server(desc=request.form['desc'], address=request.form['address'], ssl=True,
                       type=request.form['type'], port=request.form['port'])
        else:
            s = Server(desc=request.form['desc'], address=request.form['address'], ssl=False,
                       type=request.form['type'], port=request.form['port'])
        db.session.add(s)
        db.session.commit()
        return render_template('Index.html')


@main.route('/migrations', methods=['GET', 'POST'])
@authentication.admin.login_required
def migrations():
    if request.method == 'GET':
        return render_template('Migrations.html', company=Company, existing_migrations=Migration.query.all(), clientes=Company.query.all())
    elif request.method == 'POST':
        company = request.form['company']
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        m = Migration(company_id=company, start_date=start_time)
        db.session.add(m)
        db.session.commit()
        return render_template('Migrations.html', company=Company, existing_migrations=Migration.query.all(),
                               clientes=Company.query.all())


@main.route('/config/<migration_id>', methods=['PUT', 'GET', 'POST'])
@authentication.admin.login_required
def config_migration(migration_id):
    if request.method == 'POST':
        if 'put' in request.form['_method']:
            account_list = request.files['account_list']
            lista_contas = account_list.read()
            read_error_lines = None
            for linha in str(lista_contas).split('\n'):
                try:
                    if linha != '':
                        colunas = linha.split(',')
                        print colunas
                        src_server_id = colunas[0]
                        email = colunas[1]
                        src_password = colunas[2]
                        dst_password = colunas[3]
                        account = Account(src_server_id=src_server_id, migration_id=migration_id, src_email=email,
                                          src_password=src_password, dst_email=email, dst_password=dst_password,
                                          status_id=1)
                        db.session.add(account)
                        db.session.commit()

                except:
                    read_error_lines = linha+'\n'
            if read_error_lines is not None:
                response = make_response(read_error_lines)
                response.headers["Content-Disposition"] = "attachment; filename=CONTAS_EMAIL_INVALIDAS.txt"
                return response

        else:
            src_server_id = request.form['src_server_id']
            src_email = request.form['src_email']
            src_password = request.form['src_password']
            dst_email = request.form['tgt_email']
            dst_password = request.form['tgt_password']
            account = Account(src_server_id=src_server_id, migration_id=migration_id, src_email=src_email,
                              src_password=src_password, dst_email=dst_email, dst_password=dst_password, status_id=1)
            db.session.add(account)
            db.session.commit()

    c = Company.query.filter_by(id=(Migration.query.filter_by(id=migration_id).first().company_id)).first(),
    acc = Account.query.filter_by(migration_id=migration_id).all()
    return render_template('Configuration.html', cliente=c,
    accounts=acc, servers=Server.query.all(), server=Server, status=Status, message=Message)


@main.route('/config/<migration_id>/remove/<account_id>', methods=['GET'])
@authentication.admin.login_required
def remove_migration(migration_id, account_id):
    Account.query.filter_by(id=account_id).delete()
    db.session.commit()
    return redirect(url_for('main.config_migration', migration_id=migration_id))


@main.route('/config/<migration_id>/reanalyze/<account_id>', methods=['GET'])
@authentication.admin.login_required
def reanalyze_migration(migration_id, account_id):

    Account.query.filter_by(id=account_id).update({'status_id': 1})
    db.session.commit()
    return redirect(url_for('main.config_migration', migration_id=migration_id))