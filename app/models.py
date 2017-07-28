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

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from passlib.apps import custom_app_context as pwd_context


class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    folder = db.Column(db.String, nullable=False)
    message_id = db.Column(db.String, nullable=False)


class Account(db.Model):

    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    src_server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    migration_id = db.Column(db.Integer, db.ForeignKey('migration.id'), nullable=False)
    src_email = db.Column(db.String, nullable=False)
    src_password = db.Column(db.String, nullable=False)
    dst_email = db.Column(db.String, nullable=False)
    dst_password = db.Column(db.String, nullable=False)
    qtd_message = db.Column(db.Integer)
    duplicates = db.Column(db.Integer)
    without_messageid = db.Column(db.Integer)

class Server(db.Model):

    __tablename__ = 'server'

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    ssl = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.String, nullable=False)


class Status(db.Model):

    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)


class Company(db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact_number = db.Column(db.String, nullable=True)
    contact_name = db.Column(db.String, nullable=True)
    cnpj = db.Column(db.String, nullable=True)


class Migration(db.Model):

    __tablename__ = 'migration'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    start_date = db.Column(db.String, nullable=True)
    end_date = db.Column(db.String, nullable=True)


class Usuario(db.Model):

    __tablename__ = 'usuario'

    user = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String, nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __init__(self, user, password):
        self.user = user
        self.hash_password(password)
