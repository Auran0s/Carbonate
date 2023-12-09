from flask import Blueprint, render_template, session, redirect, url_for

from .home_models import *

from apps.auth.auth_api import *
from apps.user.user_models import *
from apps.stripe.stripe_api import *
from apps.stripe.stripe_models import *
from apps.translate.translate_engine import contents
from apps.instance.instance_models import *
from apps.credentials.credentials_models import *

home_renders = Blueprint('home_renders', __name__)

@home_renders.route('/')
@auth_user
@stripe_need_subscription
async def home_root_page(user):
    
    credentials_list = credentials_services_list()
    restriction = await restrictions_get_use_w_function('request', user)
    restriction_to_front = [restriction[0].uses_number, restriction[1], round((restriction[0].uses_number/restriction[1])*100)]

    return render_template('pages/page_home.html', user = user, content=contents, credentials_services_list = credentials_list, credentials_user_list = await credentials_list_by_instance(user.instances), restriction = restriction_to_front)  