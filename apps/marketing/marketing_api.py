from flask import Blueprint, request

import requests
from decouple import config

from apps.user.user_models import *

marketing_api = Blueprint('marketing_api', __name__)

def marketing_add_user(user):
    x = requests.get(config('NEWSLETTER_WEBHOOK'), params={'name':user.name, 'email':user.email}, headers={'newsletterWebhookToken':config('NEWSLETTER_WEBHOOK_TOKEN')})
    print(x)

def marketing_update_user(user):
    x = requests.get(config('NEWSLETTER_WEBHOOK'), params={'name':user.name, 'email':user.email, 'status':user.optinNL}, headers={'newsletterWebhookToken':config('NEWSLETTER_WEBHOOK_TOKEN')})
    print(x)


@marketing_api.route('/api/webhooks/marketing', methods=['POST'])
async def marketing_delete_user():
    user_email = request.json['email']

    user = await user_find_w_email(user_email)
    user = await user_optinNL(user, False)

    return 'OK', 200