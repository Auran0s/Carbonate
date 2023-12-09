from flask import Blueprint, redirect, request, url_for, session, flash, current_app

from .instance_models import *
from apps.credentials.credentials_models import credentials_find_w_instance

from apps.auth.auth_api import *

from apps.stripe.stripe_api import *

from apps.translate.translate_engine import contents

instance_api = Blueprint('instance_api', __name__)

@instance_api.route('/api/instance/auth', methods=['POST'])
async def instance_api_auth():
    if request.headers.get('Authorization') != config('API_INSTANCE_KEY'):
        return
    data = request.get_json()
    if data is not None:
        if instance_api_key := data.get('instance_api_key') is not None:
            if await instance_find_w_api_key(data.get('instance_api_key')):
                instance = await instance_find_w_api_key(data.get('instance_api_key'))
                credential = await credentials_find_w_instance(instance, data.get('credential'))
                data = {
                    "id": credential.id,
                    "name": credential.name,
                    "access_token": "secret_EQTgzpaEkhi4BZSQEyYAlmbU45gp6XRi2TYhkhHwvZq",
                }

                return jsonify({'Auth':True, 'credential':data}), 200