from app import db


class CissConfereMercadoria(db.Model):
    """
        Representa a tabela CONFERE_MERCADORIA
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'CONFERE_MERCADORIA'
    
    idautorizacao = db.Column(
        db.ForeignKey('CONFERE_AUTORIZA.idautorizacao'), 
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

    join = "and_("
    join = join + "CissProdutoGrade.idproduto == CissConfereMercadoria.idproduto,"
    join = join + "CissProdutoGrade.idsubproduto == CissConfereMercadoria.idsubproduto)"
    join_produto = join

    produto = db.relationship(
        'CissProdutoGrade',
        primaryjoin=join_produto
    )
    
    autorizacao = db.relationship(
        'CissConfereAutoriza', 
        backref=db.backref('id_autorizacao')
    )


class CissConfereAutoriza(db.Model):
    """
        Representa a tabela CONFERE_AUTORIZA
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'CONFERE_AUTORIZA'

    idautorizacao = db.Column(db.Integer, primary_key=True)
    idempresa = db.Column(db.Integer, primary_key=True)
    numnota = db.Column(db.Integer, primary_key=True)
    serienota = db.Column(db.String(3), primary_key=True)
    idclifor = db.Column( 
        db.ForeignKey('CLIENTE_FORNECEDOR.idclifor'), 
        primary_key=True
    )

    fornecedor = db.relationship(
        'CissClienteFornecedor', 
        backref=db.backref('id_fornecedor')
    )