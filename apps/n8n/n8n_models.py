from flask import redirect, url_for
from decouple import config
import httpx

from apps.instance.instance_renders import instance_service_page

N8N_TOKEN = config('N8N_TOKEN')
N8N_API_URL = config('N8N_API_URL')

def n8n_credential_create(credential):
    headers = {'Accept': 'application/json', 'X-N8N-API-KEY': N8N_TOKEN}
    body = {"name": credential.id, "type":f'{credential.name}Api', "data":{"apiKey":credential.access_token}}

    httpx.request('POST', f'{N8N_API_URL}credentials', headers=headers, json=body)

    return credential.name