import time

from datetime import date
from flask import Blueprint, render_template, redirect, url_for, current_app
from flask import request, jsonify
from flask_mail import Message
from validate_email import validate_email

# imports do app
from app.application import mycelery
from app.core.email import enviar_email

# import do formulario
from .forms import FormBuscarPendencias, FormBuscarEmailsEnviados

# import do data
from .data import buscar_pendencias_para_cobranca, buscar_emails_enviados_cobranca
from .data import buscar_pendencias_para_email, validar_pendencias_enviadas

# imports da model
from app.models.financeiro import AppEmailEnviadoCobranca
from app.models.config import ConfigFinanceiro

# import dos utils
from app.core.utils import success

# import do task
from .task import email_cobranca_task


financeiro = Blueprint('financeiro', __name__)


@financeiro.route('/cobranca/email-enviado', methods=['GET', 'POST'])
def email_cobranca_enviados():
    """
        Lista os emails de cobrança enviados aos clientes a partir
        do periodo informado
    """
    template = 'financeiro/cobranca/email-enviado/main.html'
    form = FormBuscarEmailsEnviados()
    emails = None

    if form.validate_on_submit():
        dtinicial = form.dtinicial.data
        dtfinal = form.dtfinal.data
        emails = buscar_emails_enviados_cobranca(dtinicial, dtfinal)

    content = {
        'title': 'Financeiro',
        'subtitle': 'Emails de Cobrança Enviados',
        'form': form,
        'emails': emails
    }
    return render_template(template, **content)


@financeiro.route('/cobranca/email-cobranca', methods=['GET', 'POST'])
def email_cobranca_automatica():
    """
        Envia o email de cobrança de pendencias dos clientes
    """

    template = 'financeiro/cobranca/email-cobranca/main.html'

    task = current_app.task
    clear_task = request.args.get('clear_task', None)
    if clear_task and clear_task == 'yes':
        if task and task.state == 'SUCCESS':
            current_app.task = task = None
        return redirect(url_for('financeiro.email_cobranca_automatica'))

    pendencias = None
    config = ConfigFinanceiro.by_id(1)
    has_config = True if config else False
    form = FormBuscarPendencias()

    if not task and has_config and form.validate_on_submit():
        dtinicial = form.dtinicial.data
        dtfinal = form.dtfinal.data

        pendencias = validar_pendencias_enviadas(dtinicial, dtfinal)

        # verifica se o usuario clicou em enviar para iniciar o envio dos emails
        if form.enviar.data:
            dtinicial = (dtinicial.day, dtinicial.month, dtinicial.year)
            dtfinal = (dtfinal.day, dtfinal.month, dtfinal.year)

            task = email_cobranca_task.apply_async(args=(dtinicial, dtfinal))
            current_app.task = task

            time.sleep(3)

            success('Tarefa de envio de cobranças iniciado')
            return redirect(url_for('financeiro.email_cobranca_automatica'))

    content = {
        'title': 'Financeiro',
        'subtitle': 'Email de Cobrança Automático',
        'has_config': has_config,
        'pendencias': pendencias,
        'form': form,
        'task': task
    }
    return render_template(template, **content)


def validar_email(email):
    """
        Valida se os emails nao são nulos ou inválidos
    """
    if email:
        # pega o email retornado pela base de dados e verifica se
        # nao possui mais de um email registrado e se o email
        # e valido
        email = email.split(';')
        email = [e.strip() for e in email]
        email = [e for e in email if validate_email(e)]

        if email:
            return email, 'valido'            
        else:
            # Se o email e inválido retorna False e a mensagem
            # de que o Email esta incorreto                    
            return False, 'Email(s) Incorreto(s)'
    else:
        # se nao existir nenhum email retorna False e a mensagem
        # de "Nao Possui" para ser registrado
        return False, 'Não Possui'


@financeiro.route('/task/<id>', methods=['GET'])
def get_task(id):
    """
        Retorna a task a partir do id
    """

    task = mycelery.AsyncResult(id)

    if task.info:
        return jsonify({
            'id': task.id,
            'total': task.info['total'],
            'current': task.info['current'],
            'status': task.info['status']
        })

    return 'Não existem dados', 400