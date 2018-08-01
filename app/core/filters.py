import datetime
import locale
from validate_email import validate_email


def date_format(date, format='%d/%m/%Y'):
    """
        recebe uma data e a formata no padrao informado
        ou default xx/xx/xxxx
    """
    if isinstance(date, datetime.date):
        return date.strftime(format=format)


def currency(value):
    """
        recebe uma valor float e a formata no padrao de moeda
        Reais/Brasileiro
    """
    return locale.currency(value)


def is_email_valid(email):
    """
        Recebe um email e verifica se é válido
    """
    
    if email:
        email = email.split(';')
        email = [e.strip() for e in email]
        
        for e in email:
            if validate_email(e):
                return True    
    return False


def regitry_filters(app):
    """
        registra todos os filtros criados
    """
    app.jinja_env.filters['date_format'] = date_format
    app.jinja_env.filters['currency'] = currency
    app.jinja_env.filters['is_email_valid'] = is_email_valid