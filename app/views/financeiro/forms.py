from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError
from app.core.forms import widgets as w
from datetime import date, timedelta

# import das models
from app.models.config import ConfigFinanceiro


class FormBuscarEmailsEnviados(FlaskForm):
    """
        Formulario informar a data de inicio e final
        para buscar os email de cobrança enviados
    """
    dtinicial = DateField(
        'Data Inicial', 
        format='%d/%m/%Y', 
        validators=[DataRequired(message='Iforme a data Inicial')]
    )
    dtfinal = DateField(
        'Data Final',
        format='%d/%m/%Y',
        validators=[DataRequired(message='Iforme a data Final')]
    )

    @classmethod
    def validate_dtinicial(cls, form, field):
        """
            valida se a data inicial e maior que a final
        """
        dtinicial = field.data
        dtfinal = form.dtfinal.data

        if dtinicial > dtfinal:
            raise ValidationError('A data Inicial deve ser menor ou igual a Final')

    buscar = SubmitField('Buscar')


class FormBuscarPendencias(FlaskForm):
    """
        Formulario para informar o numero da autorização
        utilizada para ajustar a tributação
    """
    dtinicial = DateField(
        'Data Inicial', 
        format='%d/%m/%Y', 
        validators=[DataRequired(message='Iforme a data Inicial.')]
    )
    dtfinal = DateField(
        'Data Final',
        format='%d/%m/%Y',
        validators=[DataRequired(message='Iforme a data Final.')]
    )

    @classmethod
    def validate_dtinicial(cls, form, field):
        """
            valida se a data inicial e maior que a final
        """
        dtinicial = field.data
        dtfinal = form.dtfinal.data

        if not dtfinal or dtinicial > dtfinal:
            raise ValidationError('A data Final deve ser maior que a Inicial.')
    
    @classmethod
    def validate_dtfinal(cls, form, field):
        """
            valida se a data final é maior ou igual a hoje
        """
        config = ConfigFinanceiro.by_id(1)
        dtfinal = field.data

        if config:
            # calcula a data para cobranca usando a (data de hoje) - (dias para cobranca)
            data_cobranca = date.today() - timedelta(config.diascobranca)
            
            if dtfinal > data_cobranca:
                data_cobranca = data_cobranca.strftime('%d/%m/%Y')
                raise ValidationError(
                    f'A data Inicial e Final deve ser menor ou igual a {data_cobranca}.'
                )

    buscar = SubmitField('Buscar')
    enviar = SubmitField('Enviar')