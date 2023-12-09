from datetime import datetime, timedelta, timezone
import jwt
from decouple import config

secret_key = config('TOKEN_SECRET_KEY')

def auth_token_activate_created(user_email):
    """Create a JWT Token for the register magic link

    Args:
        user_email (String): The user email

    Returns:
        encoded: a register magic token - is durability is 15 min.
    """
    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    playload = {"email": user_email, "token_type": "Auth_Token", 'exp': exp}
    encoded = jwt.encode(playload, secret_key, algorithm="HS256")
    return encoded

def auth_token_login_created(user_email):
    """Create a JWT Token for the login magic link

    Args:
        user_email (String): The user email

    Returns:
        encoded: a login magic token - is durability is 15 min.
    """
    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    playload = {"email": user_email, "token_type": "Login_Token", 'exp': exp}
    encoded = jwt.encode(playload, secret_key, algorithm="HS256")
    return encoded

def auth_token_JWT_created(user_email):
    """Creat a JWT Toen session for the user

    Args:
        user_email (String): The user email

    Returns:
        encoded: The JWT token è- is durability is 60min
    """
    exp = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    playload = {"email": user_email, "token_type": "JWT Token", 'exp': exp}
    encoded = jwt.encode(playload, secret_key, algorithm="HS256")
    return encoded

def auth_token_decoded(user_token):
    """Function for decoded the JWT token and his status

    Args:
        user_token (String): The JWT token of the user

    Returns:
        JSON: Return the status of the token
    """
    try:
        decoded = jwt.decode(user_token, secret_key, algorithms="HS256")
        return {'Token_Verification': True, 'playload':decoded}
    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError) as error:
        return {'Token_Verification': False, 'Error': error}