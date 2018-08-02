from datetime import date
from flask import Blueprint, render_template, redirect, url_for
from flask_mail import Message
from validate_email import validate_email

# imports do app
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
    pendencias = None
    config = ConfigFinanceiro.by_id(1)
    has_config = True if config else False
    form = FormBuscarPendencias()

    if has_config and form.validate_on_submit():
        data_envio = date.today().strftime('%d/%m/%Y')  # data de envio do email
        dtinicial = form.dtinicial.data
        dtfinal = form.dtfinal.data
        
        pendencias = validar_pendencias_enviadas(dtinicial, dtfinal)

        # verifica se o usuario clicou em enviar para iniciar o envio dos emails
        if form.enviar.data:
            pendencias_dict = buscar_pendencias_para_email(pendencias)
            
            for cliente, dados in pendencias_dict.items():
                assunto  = 'Cobrança Automatica'
                remetente = config.emailremetente
                bcc = config.emailscc.split(';') if config.emailscc else None
                pendencias_cliente = dados.get('pendencias')
                email_cliente = dados.get('email')
                enviado = True

                # valida se o(s) email(s) é valido usando validar_email()
                # e caso seja invalido email=False e mensagem=Motivo
                destinatarios, mensagem = validar_email(email_cliente)
                if destinatarios:
                    # utiliza a funcao render_template para gerar o html usado no email
                    # passando os paramametros que serao usados para preencher o html
                    # e depois faz o envio do email utlizando a funcao envia_email
                    # do pacote core.email do sistema
                    html = render_template(
                        'financeiro/cobranca/email-cobranca/mail-template.html',
                        nome=cliente,
                        data=data_envio,
                        pendencias=pendencias_cliente
                    )

                    if config.flagteste and bcc:
                        destinatarios = bcc
                        bcc = None
                    
                    enviar_email(assunto, remetente, destinatarios, html, bcc=bcc)
                else:
                    enviado = False

                # Salva os dados de envio da cobranca em AppEmailEnviadoCobranca
                # para ficar registrado o que foi enviado e quando para consulta
                # posterior
                id_cliente = dados.get('idclifor')  # id do cliente no Ciss
                for p in pendencias_cliente:
                    log_envio = AppEmailEnviadoCobranca.by(titulo=p['titulo'])
                    if not log_envio:
                        log_envio = AppEmailEnviadoCobranca()
                        log_envio.titulo = p['titulo']
                    
                    log_envio.parcela = p['parcela']
                    log_envio.dtenvio = data_envio
                    log_envio.dtvencimento = p['vencimento']
                    log_envio.valor = p['valor']
                    log_envio.idcliente = id_cliente
                    log_envio.nomecliente = cliente
                    log_envio.email = destinatarios if destinatarios else mensagem
                    log_envio.flagenviado = enviado
                    
                    log_envio.update()
        
            success('O envio das cobranças foi finalizado')
            pendencias = validar_pendencias_enviadas(dtinicial, dtfinal)
    
    content = {
        'title': 'Financeiro',
        'subtitle': 'Email de Cobrança Automático',
        'has_config': has_config,
        'pendencias': pendencias,
        'form': form
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