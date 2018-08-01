from app import db


class CissClienteFornecedor(db.Model):
    """
        Representa a tabela CLIENTE_FORNECEDOR
        do Ciss
    """
    __bind_key__ = 'ciss'
    __tablename__ = 'CLIENTE_FORNECEDOR'
    
    idclifor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    emailfinanceiro = db.Column(db.String(80), nullable=False)
    ufclifor = db.Column(db.String(2))
    tipocadastro = db.Column(db.String(1))