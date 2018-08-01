from flask import Blueprint, render_template, current_app, url_for, redirect
from flask_login import login_required
from flask_uploads import configure_uploads
from app import db

# Import dos Forms da View
from .forms import ConfigForm, ConfigFinanceiroForm

# import dos data da View
from .data import buscar_formas_pagamento

# Import das Models usadas pela View
from app.models.config import Config, ConfigFinanceiro

# import dos core
from app.core.uploads import imageSet
from app.core.utils import success


configuracoes = Blueprint('configuracoes', __name__)


@configuracoes.route('/', methods=['GET', 'POST'])
def index():
    template = 'configuracoes/main.html'
    config = Config.by_id(1)
    form = ConfigForm()

    if config and config.baseUrl and not form.baseURL.data:
        form.configId.data = config.id
        form.baseURL.data = config.baseUrl
    
    if form.validate_on_submit():
        import os
        config.baseUrl = form.baseURL.data
        
        uploadURL = os.path.join(form.baseURL.data, 'uploads')
        current_app.config.update(
            UPLOADS_DEFAULT_URL=uploadURL
        )
        configure_uploads(current_app, (imageSet, ))

        db.session.add(config)
        db.session.commit()

        success('Registro alterado com sucesso.')

    content = {
        'title': 'Configurações do Sistema',
        'form': form
    }
    return render_template(template, **content)


@configuracoes.route('/financeiro', methods=['GET', 'POST'])
def financeiro():
    """
        View que representa a interface com o usuario
        para configurar parametros usados no financeiro
    """
    template = 'configuracoes/financeiro/main.html'
    config = ConfigFinanceiro.by_id(1)
    form = ConfigFinanceiroForm()
    
    # busca as formas de pagamento do Ciss para ser usado
    # no campo de selecao de formas de pagamento usadas
    # na cobrança automatica
    formas_pagamento =  buscar_formas_pagamento()
    nome_format = lambda x: '{} - {}'.format(x.descrrecebimento, x.idrecebimento)
    formas_pagamento = [
        (int(f.idrecebimento), nome_format(f)) for f in formas_pagamento
    ]
    form.formas_pagamento.choices = formas_pagamento

    # valida o formulario
    if form.validate_on_submit():
        if not config:
            config = ConfigFinanceiro()
        
        config.diascobranca = form.dias_cobranca.data
        config.emailremetente = form.email_remetente.data
        # É necessario converter a lista de forma de pagamentos para
        # string para usar o str.join()
        lista_fmpagamento = [str(num) for num in form.formas_pagamento.data]
        config.formaspgcobranca = ','.join(lista_fmpagamento)
        if form.envia_copia.data:
            config.emailscc = form.emails_cc.data
            config.flagteste = form.flag_teste.data
        else:
            config.emailscc = None 
        config.update()

        success('Registro cadastrado com sucesso')

        return redirect(url_for('configuracoes.financeiro'))
    
    if config and not form.submit.data:
        form.dias_cobranca.data = config.diascobranca
        form.email_remetente.data = config.emailremetente
        form.formas_pagamento.data = [int(num) for num in config.formaspgcobranca.split(',')]

        if config.emailscc:
            form.envia_copia.data = True
            form.emails_cc.data = config.emailscc
            form.flag_teste.data = config.flagteste

    content = {
        'title': 'Configurações',
        'subtitle': 'Financeiro',
        'form': form
    }
    return render_template(template, **content)
