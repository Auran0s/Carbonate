from decouple import config
import httpx
import base64

from apps.credentials.credentials_models import *
from apps.n8n.n8n_models import *
from apps.instance.instance_models import *

notion_client_id = config('NOTION_OAUTH_CLIENT_ID')
notion_secret = config('NOTION_OAUTH_CLIENT_SECRET')
notion_basic = config('NOTION_OAUTH_BASIC')
APP_DOMAIN = config('APP_DOMAIN')
redirect_url = f'{APP_DOMAIN}api/credentials/callback/'

access_token_url='https://api.notion.com/v1/oauth/token'
authorize_url='https://api.notion.com/v1/oauth/authorize'

def notion_redirect_uri():
    return config('NOTION_REDIRECT_URI')

async def notion_post_code(code, user):
    """Send the recuperation token from Notion

    Args:
        code (String): the notion Oauth code
        user (User Object): the user who request this Oauth 
    """
    headers = {'Authorization': f'Basic {notion_basic}', 'Content-Type': 'application/json'}
    body = {"grant_type":"authorization_code","code":code, "redirect_uri":redirect_url}

    response = httpx.request('POST', access_token_url, headers=headers, json=body, timeout=(30, 30))

    notion_credential = response.json()
    
    instance = await instance_find_all(user)

    if 'refresh_token' in notion_credential:
        credential = await credentials_create_oauth2('notion', notion_credential['token_type'], notion_credential['access_token'], notion_credential['refresh_token'], notion_credential['expires_at'], instance.instances)
    credential = await credentials_create_oauth2('notion', notion_credential['token_type'], notion_credential['access_token'], '', 0, instance.instances)

    get_redirection = n8n_credential_create(credential)
    return get_redirection