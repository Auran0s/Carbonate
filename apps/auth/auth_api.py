from flask import Blueprint, redirect, request, url_for, session, flash, current_app
from functools import wraps
import asyncio

from apps.auth.auth_token import auth_token_decoded

from .auth_forms import *
from .auth_email import *

from apps.user.user_models import *

from apps.translate.translate_engine import contents

auth_api = Blueprint('auth_api', __name__)

def auth_user(f): # Verification if USER is connected by session named "session"
    """Auth wraps - check if user have JWT token

    Args:
        f (_type_): _description_

    Returns:
        url_for: if the user is not logged, to the auth_login_page
        wrap: keep the same page
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'session' not in session:
            return redirect(url_for('auth_login_renders.auth_login_page'))
        JWT = bytes(session['session']['JWT'], 'UTF-8')

        if auth_token_decoded(JWT)['Token_Verification'] == True:
            exp = auth_token_decoded(JWT)['playload']['exp']
            now = datetime.now(timezone.utc)
            target_time = datetime.timestamp(now + timedelta(minutes=30))
            if target_time > exp:
                session['session'] = {'JWT' : auth_token_JWT_created(auth_token_decoded(JWT)['playload']['email'])}
            user = asyncio.run(user_find_w_email(auth_token_decoded(JWT)['playload']['email']))
            if user is not None:
                user = asyncio.run(user_get_all_data(user, [Models.Customer, Models.Instances, Models.Restrictions]))
                return current_app.ensure_sync(f)(user, *args, **kwargs)
            session.pop('session', None)
            return redirect(url_for('auth_login_renders.auth_login_page'))
        else:
            flash(contents['JWT_expired'], 'errors')
            session.pop('session', None)
            return redirect(url_for('auth_login_renders.auth_login_page'))
    return wrap


def auth_get_JWT_token():
    """Function for getting the JWT token decoded

    Returns:
        email: return the email of the user contain in the JWT token
    """
    return auth_token_decoded(bytes(session['session']['JWT'], 'UTF-8'))['playload']['email']