from flask import Blueprint, render_template, session, redirect, url_for, flash

from .user_models import *
from .user_forms import *

from apps.auth.auth_api import *

from apps.stripe.stripe_api import *

from apps.translate.translate_engine import contents

user_renders = Blueprint('user_renders', __name__)

@user_renders.route('/profile')
@auth_user
@stripe_need_subscription
async def user_profile_page(user):
    Email_form = UpdateEmail(obj=user)
    form = UpdateData(obj=user)
    return render_template('pages/page_profile.html', user=user, Email_form=Email_form, form=form, content=contents)