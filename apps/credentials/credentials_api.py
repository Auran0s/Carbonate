from flask import Blueprint, redirect, request, url_for, session, flash, current_app, jsonify
from decouple import config
import yaml

from apps.auth.auth_api import *
from apps.auth.auth_email import *

from apps.marketing.marketing_api import *

from apps.translate.translate_engine import contents

from apps.instance.instance_models import instance_find_all

from .services.notion import *

from .credentials_search import *

credentials_api = Blueprint('credentials_api', __name__)

@credentials_api.route('/api/services/search/', methods=['POST'])
@auth_user
async def credentials_api_search(user):
    search_term = request.form.get('searchInput')
    if search_term is None:
        return ''
    results = search_value_in_yaml(search_term)
    sorted_results = sorted(results, key=lambda x: x['name'])
    
    instance = await instance_find_all(user)
    credentials_user_list = await credentials_list_by_instance(instance.instances)
    
    html_code = generate_html_code(sorted_results, credentials_user_list)
    return html_code

@credentials_api.route('/notion-login')
def credentials_api_notion():
    return redirect(notion_redirect_uri())

@credentials_api.route('/api/credentials/callback/')
async def credentials_api_callback():
    user = await user_find_w_email(auth_get_JWT_token())
    
    if request.args.get('code'):
        get_redirection = await notion_post_code(request.args.get('code'), user)
    else:
        return redirect(url_for('home_renders.home_root_page'))
    return redirect(url_for('instance_renders.instance_service_page', service=get_redirection)) 