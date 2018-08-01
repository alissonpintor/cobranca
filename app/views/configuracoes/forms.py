from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, IntegerField
from wtforms import SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from app.core.forms import widgets as w
from validate_email import validate_email


class ConfigForm(FlaskForm):
    """
    Formulario para alteração dos dados de Configuração do sistema
    """

    configId = HiddenField('ID', default=0)
    baseURL = StringField('URL Base', widget=w.GeInputWidget(), validators=[DataRequired()])

    submit = SubmitField('Atualizar')


class ConfigFinanceiroForm(FlaskForm):
    """
    Formulario para alteração dos dados de Configuração do Financeiro
    """
    
    render={'inputSize': 'col-md-9'}  # configura o tamanho do widget
    email_remetente = StringField(
        'Email Rementente',
        validators=[DataRequired('Iforme o Email usado para enviar a cobrança')]
    )
    dias_cobranca = IntegerField(
        'Dias para Cobrança',
        validators=[DataRequired('Iforme a quantidade de dias para cobrança')]
    )
    formas_pagamento = SelectMultipleField(
        'Forma de Pagamento',
        validators=[DataRequired('Selecione as formas de pagamento que serão cobradas')],
        coerce=int
    )
    envia_copia = BooleanField(
        'Enviar copia dos Emails'
    )
    emails_cc = StringField(
        'Email CC'
    )
    flag_teste = BooleanField(
        'Ativar Modo Teste'
    )

    @classmethod
    def validate_email_remetente(cls, form, field):
        """
            Válida se o email informado é válido
        """
        if not validate_email(field.data):
            raise ValidationError('O Email informado não é válido.')
    
    @classmethod
    def validate_emails_cc(cls, form, field):
        """
            Válida se o flag envia copia está marcado e depois
            valida se os emails para copia estao preenchidos
        """
        if form.envia_copia.data and not field.data:
            # Verifica se o flag para enviar copia esta marcado e se os
            # emails para copia foram preenchidos
            raise ValidationError('Informe o(s) email(s) para cópia.')
        
        if field.data:
            # Se os emails de copias foram preenchidos valida se todos eles
            # são emails validos
            emails = field.data
            emails = emails.split(';')
            emails = [email.strip() for email in emails]

            for email in emails:
                is_valid = validate_email(email)
                if not is_valid:
                    raise ValidationError('Um ou mais Emails de cópia são inválidos.')


    submit = SubmitField('Atualizar')
