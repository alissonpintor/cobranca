from app.application import db
from datetime import date, datetime


class CissOrcamento(db.Model):
    """
        Representa a tabela ORCAMENTO
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'ORCAMENTO'

    idempresa = db.Column(db.Integer, primary_key=True)
    idorcamento = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    observacao = db.Column(db.String(600))
    dtmovimento = db.Column(db.DateTime())
    idclifor = db.Column(
        db.Integer,
        db.ForeignKey('CLIENTE_FORNECEDOR.idclifor')
    )


class CissOrcamentoProd(db.Model):
    """
        Representa a tabela ORCAMENTO_PROD
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'ORCAMENTO_PROD'

    idempresa = db.Column(db.Integer, primary_key=True)
    idproduto = db.Column(
        db.ForeignKey('PRODUTO_GRADE.idproduto'), 
        primary_key=True
    )
    idsubproduto = db.Column(
        db.ForeignKey('PRODUTO_GRADE.idsubproduto'), 
        primary_key=True
    )
    idorcamento = db.Column(
        db.ForeignKey('ORCAMENTO.idorcamento'),
        primary_key=True
    )
    qtdproduto = db.Column(db.Numeric(12,3))
    idvendedor = db.Column(db.Integer)
    valtotliquido = db.Column(db.Numeric(14,2))


class CissPreVenda(db.Model):
    """
        Representa a tabela PRE_VENDA
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'PRE_VENDA'

    idempresa = db.Column(db.Integer, primary_key=True)
    idprevenda = db.Column(db.Integer, primary_key=True)
    dtmovimento = db.Column(db.Date(), primary_key=True)
    nome = db.Column(db.String(80))
    observacao = db.Column(db.String(600))
    flagimportado = db.Column(
        db.String(1),
        db.CheckConstraint("flagimportado='T' or flagimportado='F'")
    )
    idclifor = db.Column(
        db.Integer,
        db.ForeignKey('CLIENTE_FORNECEDOR.idclifor')
    )


class CissPreVendaProd(db.Model):
    """
        Representa a tabela PRE_VENDA_PROD
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'PRE_VENDA_PROD'

    idempresa = db.Column(db.Integer, primary_key=True)
    dtmovimento = db.Column(db.Date(), primary_key=True)
    idprevenda = db.Column(
        db.Integer,
        db.ForeignKey('PRE_VENDA.idprevenda'),
        primary_key=True
    )
    idproduto = db.Column(
        db.ForeignKey('PRODUTO_GRADE.idproduto'), 
        primary_key=True
    )
    idsubproduto = db.Column(
        db.ForeignKey('PRODUTO_GRADE.idsubproduto'), 
        primary_key=True
    )