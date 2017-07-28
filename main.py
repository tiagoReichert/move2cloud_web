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

import os
from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.models import db
from app.models import Usuario, Status


# default to dev config because no one should use this in
# production anyway
env = os.environ.get('APP_ENV', 'dev')
app = create_app('app.settings.%sConfig' % env.capitalize())

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))


@manager.command
def createdb(passwd):
    """ Creates a database with all of the tables defined in
        your SQLAlchemy models
    """
    db.create_all()
    u = Usuario('admin', passwd)
    db.session.add(u)
    s1 = Status(description='CRIADO')
    db.session.add(s1)
    s2 = Status(description='MIGRANDO')
    db.session.add(s2)
    s3 = Status(description='CONCLUIDO')
    db.session.add(s3)
    s4 = Status(description='ERRO')
    db.session.add(s4)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
