from app.application import db
from datetime import date, datetime


class CissNcm(db.Model):
    """
        Representa a tabela NCM
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'NCM'

    ncm = db.Column(db.String(8), primary_key=True)
    descricao = db.Column(db.String(820))
    flagcargatributariamedia = db.Column(
        db.String(1), 
        db.CheckConstraint("flagcargatributariamedia=='T' or flagcargatributariamedia=='F'")
    )
  

class CissProduto(db.Model):
    """
        Representa a tabela PRODUTO
        do Ciss
    """
    __tablename__ = 'PRODUTO'
    __bind_key__ = 'ciss'

    idproduto = db.Column(db.Integer, primary_key=True)
    descrcomproduto = db.Column(db.String(60))
    fabricante = db.Column(db.String(40))
    embalagemsaida = db.Column(db.String(2), db.ForeignKey(
        'PRODUTO_EMBALAGEM.unidadeembalagem'))
    
    embalagem = db.relationship('CissEmbalagens')


class CissEmbalagens(db.Model):
    """
        Representa a tabela PRODUTO_EMBALAGEM
        do Ciss
    """
    __tablename__ = 'PRODUTO_EMBALAGEM'
    __bind_key__ = 'ciss'

    unidadeembalagem = db.Column(db.String(2), primary_key=True)
    descrembalagem = db.Column(db.String(40))


class CissProdutoGrade(db.Model):
    """
        Representa a tabela PRODUTO_GRADE
        do Ciss
    """
    __tablename__ = 'PRODUTO_GRADE'
    __bind_key__ = 'ciss'

    idproduto = db.Column(db.ForeignKey('PRODUTO.idproduto'), primary_key=True)
    idsubproduto = db.Column(db.Integer, primary_key=True)
    subdescricao = db.Column(db.String(100))
    descrresproduto = db.Column(db.String(60))
    codbar = db.Column(db.String(20))
    idmodelo = db.Column(db.Integer)
    idtipo = db.Column(db.Integer)
    pesoliquido = db.Column(db.Numeric(12,3))
    valmultivendas = db.Column(db.Numeric(12,3))
    dtcadastro = db.Column(db.Date())
    ncm = db.Column(db.ForeignKey('NCM.ncm'))
    flaginativo = db.Column(db.String(1), db.CheckConstraint(
        "flaginativo='T' or flaginativo='F'"))

    produto = db.relationship('CissProduto')

    join = "and_("
    join = join + "CissProdutoGrade.idproduto == CissConfereMercadoria.idproduto,"
    join = join + "CissProdutoGrade.idsubproduto == CissConfereMercadoria.idsubproduto)"
    join_confere_mercadoria = join
    
    confere_mercadoria = db.relationship(
        'CissConfereMercadoria',
        primaryjoin=join_confere_mercadoria,
        backref='produto_grade_confere'
    )

    join = "and_("
    join = join + "CissProdutoGrade.idproduto == CissProdutoTributacao.idproduto,"
    join = join + "CissProdutoGrade.idsubproduto == CissProdutoTributacao.idsubproduto)"
    join_produto_tributacao = join

    produto_tributacao = db.relationship(
        'CissProdutoTributacao',
        primaryjoin=join_produto_tributacao,
        backref='produto_grade_tributacao'
    )

    join = "and_("
    join = join + "CissProdutoGrade.idproduto == CissProdutoFornecedor.idproduto,"
    join = join + "CissProdutoGrade.idsubproduto == CissProdutoFornecedor.idsubproduto)"
    join_codigo_fornecedor = join

    codigo_fornecedor = db.relationship(
        'CissProdutoFornecedor',
        primaryjoin=join_codigo_fornecedor,
        backref='produto_grade'
    )

    join = "and_(CissNcm.ncm == CissProdutoGrade.ncm)"
    join_ncm_produto = join
    
    ncm_produto = db.relationship(
        'CissNcm',
        primaryjoin=join_ncm_produto,
        backref='produtos'
    )


class CissProdutoEstoque(db.Model):
    """
        Representa a tabela ESTOQUE_SALDO_ATUAL
        do Ciss
    """
    __tablename__ = 'ESTOQUE_SALDO_ATUAL'
    __bind_key__ = 'ciss'

    idproduto = db.Column(db.ForeignKey('PRODUTO_GRADE.idproduto'), 
                          primary_key=True)
    idsubproduto = db.Column(db.ForeignKey('PRODUTO_GRADE.idsubproduto'), 
                          primary_key=True)
    idlocalestoque = db.Column(db.Integer, primary_key=True)
    idempresa = db.Column(db.Integer, primary_key=True)
    qtdatualestoque = db.Column(db.Numeric(12,3))
    dtalteracao = db.Column(db.DateTime())

    join = "and_("
    join = join + "CissProdutoEstoque.idproduto==CissProdutoGrade.idproduto,"
    join = join + "CissProdutoEstoque.idsubproduto==CissProdutoGrade.idsubproduto,"
    join = join + "CissProdutoEstoque.idlocalestoque==1,"
    join = join + "CissProdutoEstoque.idempresa==2)"

    produto = db.relationship(
        'CissProdutoGrade',
        backref='saldo',
        primaryjoin=join
    )


class CissProdutoPreco(db.Model):
    """
        Representa a tabela POLITICA_PRECO_PRODUTO
        do Ciss
    """
    __tablename__ = 'POLITICA_PRECO_PRODUTO'
    __bind_key__ = 'ciss'

    idproduto = db.Column(db.ForeignKey('PRODUTO_GRADE.idproduto'), 
                          primary_key=True)
    idsubproduto = db.Column(db.ForeignKey('PRODUTO_GRADE.idsubproduto'), 
                             primary_key=True)
    idempresa = db.Column(db.Integer, primary_key=True)
    valprecovarejo = db.Column(db.Numeric(15, 6))
    valpromvarejo = db.Column(db.Numeric(15, 6))
    dtinipromocaovar = db.Column(db.Date())
    dtfimpromocaovar = db.Column(db.Date())

    join = "and_("
    join = join + "CissProdutoPreco.idproduto==CissProdutoGrade.idproduto,"
    join = join + "CissProdutoPreco.idsubproduto==CissProdutoGrade.idsubproduto,"
    join = join + "CissProdutoPreco.idempresa==2)"

    produto = db.relationship(
        'CissProdutoGrade',
        backref='preco',
        primaryjoin=join
    )


class CissProdutoTributacao(db.Model):
    """
        Representa a tabela PRODUTO_TRIBUTACAO_ESTADO
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'PRODUTO_TRIBUTACAO_ESTADO'
    
    uf = db.Column(db.String(2), primary_key=True)
    idproduto = db.Column(
        db.ForeignKey('PRODUTO_GRADE.idproduto'), 
        primary_key=True
    )
    idsubproduto = db.Column(
        db.ForeignKey('PRODUTO_GRADE.idsubproduto'), 
        primary_key=True
    )
    pericment = db.Column(db.Integer())
    pericmsubst = db.Column(db.Integer())
    permargemsubsti = db.Column(db.Integer())
    permargemsubstisai = db.Column(db.Integer())
    idsittribent = db.Column(db.Integer())
    tiposittribent = db.Column(db.Integer())


class CissProdutoFornecedor(db.Model):
    """
        Representa a tabela PRODUTO_FORNECEDOR
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'PRODUTO_FORNECEDOR'

    idclifor = db.Column(
        db.Integer(),
        db.ForeignKey('CLIENTE_FORNECEDOR.idclifor'), 
        primary_key=True
    )
    idproduto = db.Column(
        db.Integer(),
        db.ForeignKey('PRODUTO_GRADE.idproduto'), 
        primary_key=True
    )
    idsubproduto = db.Column(
        db.Integer(),
        db.ForeignKey('PRODUTO_GRADE.idsubproduto'), 
        primary_key=True
    )
    
    codigointernoforn = db.Column(db.String(60))

    fornecedor = db.relationship('CissClienteFornecedor')
