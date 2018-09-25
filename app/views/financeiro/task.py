from datetime import date
from flask import render_template
from app import db
from app.application import mycelery, app
from app.log import Log
from validate_email import validate_email

# import do models
from app.models.config import ConfigFinanceiro
from app.models.financeiro import AppEmailEnviadoCobranca

# imrpot dos utils
from app.core.email import enviar_email

# import dos filters
from .filter import validar_pendencias_enviadas, buscar_pendencias_para_email


@mycelery.task(bind=True, name='envia-email-cobranca')
def email_cobranca_task(self, dtinicial, dtfinal):
    """
        Task para enviar os emails de cobranca

        Params
        ---------
        dtinicial: Date
            Data inicial para buscar as pendencias em aberto para o envio dos
            email
        dtfinal: Date
            Data Final para buscar as pendencias em aberto para o envio dos
            email
    """

    with app.app_context():
        db.engine.dispose()
        config = ConfigFinanceiro.by_id(1)
        data_envio = date.today().strftime('%d/%m/%Y')  # data de envio do email
        dtinicial = date(day=dtinicial[0], month=dtinicial[1], year=dtinicial[2])
        dtfinal = date(day=dtfinal[0], month=dtfinal[1], year=dtfinal[2])

        pendencias = validar_pendencias_enviadas(dtinicial, dtfinal)
        pendencias = buscar_pendencias_para_email(pendencias)

        count = 1
        total = len(pendencias)

        Log.info('[CONBRANÇA] Iniciando o envio dos emails')
        for cliente, dados in pendencias.items():
            Log.info(f'[CONBRANÇA] Enviando o email do cliente {cliente}')

            self.update_state(
                state='PROGRESS',
                meta={
                    'current': count,
                    'total': total,
                    'status': 'Enviando o cliente {}'.format(cliente)
                }
            )

            assunto = 'Cobrança Automatica'
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

                Log.info(f'[CONBRANÇA]------ Email enviado com sucesso')
            else:
                Log.info(f'[CONBRANÇA]------ Email não enviado. Cliente sem emails válidos')
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

            Log.info(f'[CONBRANÇA]------ Evento registrado no sistema')

            count += 1

        Log.info('[CONBRANÇA] Envio dos emails finalizado.')

    return {
        'current': total,
        'total': total,
        'status': 'complete'
    }


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
