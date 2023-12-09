from flask import Blueprint, render_template, session, redirect, url_for, flash

from .auth_forms import *
from .auth_token import *

from apps.home.home_renders import *

from apps.user.user_models import *
from apps.stripe.stripe_api import *

auth_renders = Blueprint('auth_renders', __name__,
template_folder='templates')

@auth_renders.route('/logout')
def auth_logout_page():
    session.pop('session', None)
    return redirect(url_for('auth_login_renders.auth_login_page'))