import locale
from app import assets, db, loginManager, mail
from app.bundles import css, js
from app.config import app_config

from flask import Flask, send_from_directory, request, render_template
from flask import request_finished, redirect, url_for, make_response
from flask_login import current_user
from flask_migrate import Migrate
from flask_uploads import configure_uploads
from flask_babel import Babel

from app.core.celery_app import Task


#Configura a Moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# def create_app():
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config['dev'])
app.config.from_pyfile('config.py')

assets.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

# Iniciao o Flask Mail
mail.init_app(app)

assets.register('css', css)
assets.register('js', js)

# Incia o Celery
Task.set_celery(app)
mycelery = Task.get_celery()
from app.core import tasks

# Inicia o Login Manager
loginManager.init_app(app)

# imports do core
from app.core.errorhandler import createErrorHandler
createErrorHandler(app)

# Importa as Blueprints
from app.views.index import bp
from app.views.account.views import account
from app.views.configuracoes import configuracoes
from app.views.financeiro import financeiro

# Registra as Blueprints
app.register_blueprint(bp, url_prefix='/')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(configuracoes, url_prefix='/configuracoes')
app.register_blueprint(financeiro, url_prefix='/financeiro')

# importa e registra os filtros criados para usar no jinja
from app.core.filters import regitry_filters
regitry_filters(app)

# Importa as Models
from app.models import access, config, clientes
from app.models import produtos, views, compras

# Correção do erro de Conexão Perdida do SQLAlchemy
from app.core.sqlalchemyerror import sqlalchemyErrorHandler

with app.app_context():
    # Cria o Banco de Dados
    db.create_all(bind=None)
    sqlalchemyErrorHandler(db)
    
    # Cria o usuario admin se não existe
    if not access.User.hasAdmin():
        access.User.createAdmin()
        access.User.createValdecir()
    
    # Cria configuração inicial do App
    if not config.Config.hasCreated():
        config.Config.createConfig()
    else:
        if (not app.config['UPLOADS_DEFAULT_URL'] 
                and config.Config.hasBaseUrl()):
            
            import os
            uploadURL = os.path.join(config.Config.hasBaseUrl(), 
                                    'uploads')
            app.config['UPLOADS_DEFAULT_URL'] = uploadURL


@app.before_request
def verificar_parametros():
    # Verifica se os parametros do Magento Existem e caso
    # negativo o usuario é redirecionado para a tela de
    # configurações do magento
    from app.models.config import Config
    from app.core.utils import warning
    from app.views.configuracoes.views import index

    allowed_paths = [
        '/logout',
        '/integrador/produtos/imagens/enviar'
    ]

    parametros = Config.by_id(1)
    is_authenticated = current_user.is_active and current_user.is_authenticated
    path = request.path

    if parametros:
        parametros = True if parametros.baseUrl else False
    
    if is_authenticated and not parametros and path not in allowed_paths:
        warning('A URL base do sistema deve ser configurada.')
        return make_response(index())


# Configura o Flask-Uploads para upload de arquivos e fotos
from app.core.uploads import imageSet, planilhaSet
configure_uploads(app, (imageSet, planilhaSet))

@app.route('/uploads/<path>/<filename>')
def uploaded_file(path, filename):
    import os
    folder = os.path.join(app.config['UPLOAD_FOLDER'], path)
    return send_from_directory(folder, filename)

# Configura o Babel para traduções
babel = Babel(app)

@babel.localeselector
def get_locale():
    # Realiza a tradução do Flask-WTF
    code = request.args.get('lang', 'pt')
    return code