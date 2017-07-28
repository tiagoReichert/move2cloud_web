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

from flask_httpauth import HTTPBasicAuth
from app.models import Usuario
admin = HTTPBasicAuth()

@admin.verify_password
def verify_token(user, password):
    u = Usuario.query.filter_by(user=user).first()
    if u:
        if u.verify_password(password):
            return True
    return False

