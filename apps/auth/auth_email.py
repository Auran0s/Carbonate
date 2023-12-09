import requests
from decouple import config


from apps.user.user_models import *
from .auth_token import *

def auth_email_register(user_email):
    """Send the register magic link by email to the user

    Args:
        user_email (String): get the email of the user
    """
    token = auth_token_activate_created(user_email)

    x = requests.get(config('MAIL_WEBHOOK_REGISTER'), params={'token':f"{config('APP_DOMAIN')}register/activate/{token}", 'email':user_email}, headers={'mailWebhookToken':config('MAIL_WEBHOOK_TOKEN')})

    print(f"{config('APP_DOMAIN')}register/activate/{token} email:{user_email}")
    
    
def auth_email_login(user_email):
    """Send the login magic link by email to the user

    Args:
        user_email (String): get the email of the user
    """
    token = auth_token_login_created(user_email)

    x = requests.get(config('MAIL_WEBHOOK_LOGIN'), params={'token':f"{config('APP_DOMAIN')}login/activate/{token}", 'email':user_email}, headers={'mailWebhookToken':config('MAIL_WEBHOOK_TOKEN')})

    print(f"{config('APP_DOMAIN')}login/activate/{token} email':{user_email}")