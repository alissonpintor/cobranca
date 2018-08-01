"""
    !/usr/bin/env python
    -*- coding: utf-8 -*-
    
    modulo que contem as funcoes para envio de email
    do app Stoky
"""
from app import mail
from app.application import app
from flask_mail import Message


def enviar_email(assunto, remetente, destinatarios, html, bcc=None, anexos=None):
    """
        Funcao que recebe o assunto, remetente, destitarios,
        o corpo do email e o html do email e envia
    """

    # cria a mensagem de email com os dados informados
    mensagem = Message(
        assunto,
        sender=remetente,
        recipients=destinatarios,
        html=html,
        bcc=bcc
    )

    # adiciona anexos se existir algum
    if anexos:
        with app.open_resource('static/img/logo.png') as img:
            mensagem.attach('logo.png', 'image/png', img.read())

    # Envia o email usando o flask_mail criado para o app
    mail.send(mensagem)

    