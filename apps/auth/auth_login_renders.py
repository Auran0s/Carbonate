from flask import Blueprint, render_template, session, redirect, url_for, flash

from .auth_forms import *
from .auth_token import *

from apps.home.home_renders import *

from apps.user.user_models import *
from apps.stripe.stripe_api import *

from apps.translate.translate_engine import contents

auth_login_renders = Blueprint('auth_login_renders', __name__)

@auth_login_renders.route('/login')
async def auth_login_page():
    """Auth login page

    Returns:
        template: login.html template
    """
    if session.get('session') is not None:
        return redirect(url_for('home_renders.home_root_page'))
    form = LoginForm()
    return render_template('pages/page_login.html', form=form, title='Login', content=contents)

@auth_login_renders.route('/api/auth/login', methods=['POST'])
async def auth_login():
    """Auth login API endpoint

    Returns:
        url_for: redirect to the auth_login_page
    """
    form = LoginForm(request.form)
    if form.validate():
        if user := await user_find_w_email(form.email.data):
            auth_email_login(user.email)
            flash(contents['auth_login_email_exist'], 'success')
            return redirect(url_for('auth_login_renders.auth_login_page'))
        flash(contents['auth_login_email_exist'], 'success')
        return redirect(url_for('auth_login_renders.auth_login_page'))
    flash(form.email.errors[0], 'errors')
    return redirect(url_for('auth_login_renders.auth_login_page'))

@auth_login_renders.route('/login/activate/<token>')
async def auth_login_token_page(token):
    """Magic link login endpoint

    Args:
        token (String UUID): the JWT token register in the cookie from the user session

    Returns:
        url_for: redirect to the auth_login_page
    """
    if auth_token_decoded(token)['Token_Verification'] == True and auth_token_decoded(token)['playload']['token_type'] == 'Login_Token':
        user_email = auth_token_decoded(token)['playload']['email']
        session['session'] = {'JWT' : auth_token_JWT_created(user_email)}
        return redirect(url_for('home_renders.home_root_page'))
    flash(contents['JWT_expired'], 'succes')
    return redirect(url_for('auth_login_renders.auth_login_page'))