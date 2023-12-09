from flask import Blueprint, redirect, request, url_for, session, flash, current_app

from .user_forms import *
from .user_models import *

from apps.auth.auth_api import *
from apps.auth.auth_email import *

from apps.marketing.marketing_api import *

from apps.translate.translate_engine import contents

user_api = Blueprint('user_api', __name__)


@user_api.route('/api/user/update/email', methods=['POST'])
async def user_api_update_email():
    user = await user_find_w_email(auth_get_JWT_token())
    form = UpdateEmail(request.form)
    if form.validate():
        if await user_find_w_email(form.email.data) is None:
            await user_email_update(user, form.email.data)
            session.pop('session', None)
            return redirect(url_for('auth_login_renders.auth_login_page'))
        else:
            flash(contents['user_profile_email_exist'], 'errors')
            return redirect(url_for('user_renders.user_profile_page'))  
    else:
        flash(f'{form.email.errors[0]}', 'errors')
        return redirect(url_for('user_renders.user_profile_page'))


@user_api.route('/api/user/update/data', methods=['POST'])
async def user_api_update_optinNL():
    user = await user_find_w_email(auth_get_JWT_token())
    form = UpdateData(request.form)
    if form.validate():
        if user.optinNL is False:
            user = await user_optinNL(user, form.optinNLFalse.data)
        else:
            user = await user_optinNL(user, form.optinNLTrue.data)
        marketing_update_user(user)
        data = {
            'name': form.name.data,
            'surname': form.surname.data
        }
        await user_update_data(user, data)
    return redirect(url_for('user_renders.user_profile_page'))