from flask import Blueprint, render_template, session, redirect, url_for, flash

from .auth_forms import *
from .auth_token import *

from apps.home.home_renders import *

from apps.user.user_models import *
from apps.stripe.stripe_api import *
from apps.instance.instance_models import *

from apps.translate.translate_engine import contents

auth_register_renders = Blueprint('auth_register_renders', __name__,
template_folder='templates')

@auth_register_renders.route('/register')
async def auth_register_page():
    if session.get('session') is not None:
        return redirect(url_for('home_renders.home_root_page'))
    form = RegisterForm()
    return render_template('pages/page_register.html', form=form, title="Register", content=contents)

@auth_register_renders.route('/api/auth/register', methods=['POST'])
async def auth_register():
    form = RegisterForm(request.form)
    if form.validate():
        if await user_find_w_email(form.email.data):
            flash(contents['auth_register_already_account'], 'errors')
            return redirect(url_for('auth_register_renders.auth_register_page'))
        user = await user_create(form.email.data, form.name.data, form.surname.data)
        await stripe_create_customer(user)
        await instance_create(user)
        if form.optinNL.data == True:
            await user_optinNL(user, form.optinNL.data)
        flash(contents["auth_register_link_sended"], 'success') #Add email function
        auth_email_register(form.email.data)
        return redirect(url_for('auth_register_renders.auth_register_page'))
    else:
        if form.email.errors:
            flash(form.email.errors[0], 'email_errors')
        elif form.name.errors:
            flash(form.name.errors[0], 'name_errors')
        elif form.surname.errors:
            flash(form.surname.errors[0], 'surname_errors')
        else:
            flash(form.terms.errors[0], 'terms_errors')
    return redirect(url_for('auth_register_renders.auth_register_page'))

@auth_register_renders.route('/register/activate/<token>')
async def auth_activate_account_page(token):
    if auth_token_decoded(token)['Token_Verification'] == True and auth_token_decoded(token)['playload']['token_type'] == 'Auth_Token':
        user_email = auth_token_decoded(token)['playload']['email']
        user = await user_activate(user_email, True) #Activate the USER
        if user is not None:
            session['session'] = {'JWT' : auth_token_JWT_created(user_email)}
            return redirect(url_for('stripe_renders.stripe_choice_subscription_page'))
    flash(contents["JWT_expired"], 'succes')
    return redirect(url_for('auth_login_renders.auth_login_page'))