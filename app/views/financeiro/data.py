import locale
from datetime import date, timedelta
from app import db

#import das Models
from app.models.config import ConfigFinanceiro
from app.models.financeiro import CissViewContasReceber, AppEmailEnviadoCobranca
from app.models.clientes import CissClienteFornecedor


def buscar_emails_enviados_cobranca(dtinicial, dtfinal):
    """
        Busca os email de cobranca que foram enviados no
        periodo informado
    """
    emails = AppEmailEnviadoCobranca.query.filter(
        AppEmailEnviadoCobranca.dtenvio.between(
            dtinicial,
            dtfinal
        )
    ).all()

    return emails


def buscar_pendencias_para_cobranca(dtinicial, dtfinal):
    """
        busca contas a receber que estao em aberto no
        periodo informado
    """
    # busca as pendencias na data_busca que ainda estao em aberto
    # no sistema das formas de pagamento informadas e que a origem
    # seja notas fiscal de saida NFS.
    config = ConfigFinanceiro.by_id(1)
    formas_pagamento = [int(cod) for cod in config.formaspgcobranca.split(',')]

    pendecias = db.session.query(
        CissViewContasReceber.dtvencimento,
        CissViewContasReceber.digitotitulo,
        CissViewContasReceber.idtitulo,
        CissViewContasReceber.valtitulo,
        CissClienteFornecedor.idclifor,
        CissClienteFornecedor.nome,
        CissClienteFornecedor.email
    ).join(
        CissViewContasReceber.cliente
    ).filter(
        CissViewContasReceber.origemmovimento == 'NFS',
        CissViewContasReceber.flagbaixada == 'F',
        CissViewContasReceber.idrecebimento.in_(formas_pagamento),
        CissViewContasReceber.dtvencimento.between(
            dtinicial,
            dtfinal
        )
    ).order_by(
        CissClienteFornecedor.nome,
        CissViewContasReceber.digitotitulo,
        CissViewContasReceber.idtitulo
    ).all()

    return pendecias


class Kwargs():
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


def validar_pendencias_enviadas(dtinicial, dtfinal):
    """
    """
    busca = buscar_pendencias_para_cobranca(dtinicial, dtfinal)
    pendencias = []

    for p in busca:
        enviada = db.session.query(
            AppEmailEnviadoCobranca.flagenviado
        ).filter(
            AppEmailEnviadoCobranca.titulo == p.idtitulo,
            AppEmailEnviadoCobranca.parcela == p.digitotitulo
        ).first()
        
        data = Kwargs(
            **{field: getattr(p, field) for field in p._fields}
        )
        setattr(data, 'enviado', enviada.flagenviado if enviada else False)

        pendencias.append(data)
    
    return pendencias


def buscar_pendencias_para_email(data):
    """
        busca as pendecias para envio do email e a converte
        para dict para agrupar as pendencias por cliente
    """
    pendecias = {}  # dict que vai conter as pendencias
    for p in data:        
        cliente = pendecias.setdefault(p.nome.title(), {})
        cliente.setdefault('email', p.email)
        cliente.setdefault('idclifor', p.idclifor)
        pendencia = cliente.setdefault('pendencias', [])
        pendencia.append(
            {
                'titulo': p.idtitulo,
                'parcela': p.digitotitulo,
                'vencimento': p.dtvencimento.strftime("%d/%m/%Y"),
                'valor': str(locale.currency(p.valtitulo))
            }
        )

    return pendecias