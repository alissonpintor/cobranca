from app import db


class AppEmailEnviadoCobranca(db.Model):
    """
        Tabela que contem os email de cobranca automatica
        enviado pelo sistema
    """
    __tablename__ = 'tbl_email_enviado_cobranca'

    idenvio = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Integer)
    parcela = db.Column(db.Integer)
    dtenvio = db.Column(db.Date())
    dtvencimento = db.Column(db.Date())
    valor = db.Column(db.String(30))
    idcliente = db.Column(db.Integer)
    nomecliente = db.Column(db.String(80))
    email = db.Column(db.String(80))
    flagenviado = db.Column(db.Boolean())


class CissFormaPagamento(db.Model):
    """
        Representa a View FORMA_PAGREC
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'FORMA_PAGREC'

    idrecebimento = db.Column(db.Integer, primary_key=True)
    descrrecebimento = db.Column(db.String(40))


class CissViewContasReceber(db.Model):
    """
        Representa a View CONTAS_RECEBER_SALDOS_VIEW
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'CONTAS_RECEBER_SALDOS_VIEW'
    
    idempresa = db.Column(db.Integer, primary_key=True)
    idtitulo = db.Column(db.Integer, primary_key=True)
    digitotitulo = db.Column(db.Integer, primary_key=True)
    origemmovimento = db.Column(db.String(5))
    dtmovimento = db.Column(db.Date())
    dtvencimento = db.Column(db.Date())
    valliquidotitulo = db.Column(db.Numeric(12,3))
    valtitulo = db.Column(db.Numeric(12,3))
    
    flagbaixada = db.Column(
        db.String(1), 
        db.CheckConstraint("flagbaixada='T' or flagbaixada='F'")
    )
    idclifor = db.Column(
        db.Integer, 
        db.ForeignKey('CLIENTE_FORNECEDOR.idclifor'),
        primary_key=True
    )
    idrecebimento = db.Column(
        db.Integer,
        db.ForeignKey('FORMA_PAGREC.idrecebimento')
    )

    # relacionamento que possui o cliente da relação com CLIENTE_FORNECEDOR
    cliente = db.relationship(
        'CissClienteFornecedor'
    )