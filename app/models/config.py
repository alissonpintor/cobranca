from app import db


class Config(db.Model):
    """
    Create an Config App table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    baseUrl = db.Column(db.String(200))

    @classmethod
    def hasCreated(cls):
        exist = cls.query.filter_by(id=1).first()
        return True if exist else False
    
    @classmethod
    def createConfig(cls):
        config = cls()
        config.baseUrl = None

        db.session.add(config)
        db.session.commit()
    
    @classmethod
    def hasBaseUrl(cls):
        config = cls.query.filter_by(id=1).first()
        return config.baseUrl


class ConfigFinanceiro(db.Model):
    """
        Configurações do módulo financeiro
    """
    __tablename__ = 'config_financeiro'

    id = db.Column(db.Integer, primary_key=True)
    emailremetente = db.Column(db.String(200))
    diascobranca = db.Column(db.Integer)
    formaspgcobranca = db.Column(db.String(200))
    emailscc = db.Column(db.String(200))
    flagteste = db.Column(db.Boolean)