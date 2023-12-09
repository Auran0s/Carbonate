from flask import Blueprint, render_template, session, redirect, url_for
from jinja2 import Environment, FileSystemLoader

from apps.auth.auth_api import *
from apps.user.user_models import *
from apps.stripe.stripe_api import *
from apps.translate.translate_engine import contents
from apps.instance.instance_models import *
from apps.credentials.credentials_models import credentials_services_list, credentials_list_by_instance, credentials_find_w_instance

instance_renders = Blueprint('instance_renders', __name__)

@instance_renders.route('/integrations/s/<service>')
@auth_user
@stripe_need_subscription
async def instance_service_page(user, service=None):

    credential = await credentials_find_w_instance(user.instances, service)
    credentials_list = credentials_services_list()
    restriction = await restrictions_get_use_w_function('request', user)
    restriction_to_front = [restriction[0].uses_number, restriction[1], round((restriction[0].uses_number/restriction[1])*100)]
        
    return render_template('pages/page_service.html', user = user, content=contents, service=service, credential=credential, service_data=find_service_by_name(credentials_list, service), restriction = restriction_to_front)

def find_service_by_name(service_list, target_name):
    return next(
        (
            service
            for service in service_list
            if service['name'].lower() == target_name.lower()
        ),
        None,
    )