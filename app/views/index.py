from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

# Import do Form de Login
from app.views.forms import LoginForm

# import dos Models utlizados na View
from app.models.access import User

# import dos Utils
from app.core.utils import success, warning, error, info


bp = Blueprint('bp', __name__)


@bp.route('/', methods=['GET','POST'])
def login():
    """
        View da Tela de Lgin do sistema
    """

    form = LoginForm()

    if current_user.is_active and current_user.is_authenticated:
        return redirect(request.args.get('next') or url_for('bp.index'))

    if form.validate_on_submit():
        # Busca o Usuario pelo Username Informado
        username = form.username.data.lower().strip()
        user = User.query.filter_by(userName=username).first()

        # Verifica se o Usuário Existe e se a Senha está correta
        if user and user.verifyPassword(form.password.data):
            # Faz o Login do usuário
            login_user(user)
            success('Login efetuado com sucesso.')
            
            # Redireciona o Usuario para a tela Principal ou a Tela desejada
            return redirect(request.args.get('next') or url_for('bp.index'))
        
        # when login details are incorrect
        else:
            warning('Usuário ou senha inválido.')            
    
    content = {
        'title': 'Tela de Login',
        'form': form
    }
    return render_template('login.html', **content)


@bp.route('logout')
def logout():
    """
        View Responsavel por realizar o Logout do Usuário
    """
    logout_user()
    success('Logged out efetuado com sucesso.')

    # redirect to the login page
    return redirect(url_for('bp.login'))


@bp.route('inicio')
def index():
    """
        View Inicial do sistema
    """
    template = 'index.html'
    result = {
        'title': 'Seja Bem Vindo'
    }
    # redirect to the login page
    return render_template(template, **result)

