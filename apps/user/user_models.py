from prisma import Prisma

from hashlib import md5
from datetime import datetime

class Models:
    Customer = "customer"
    Restrictions = "restrictions"
    Instances = "instances"
    Collections = "Collections"

async def user_create(email, name, surname):
    """User create

    Args:
        email (str): User email
        name (str): User name
        surname (str): user surname

    Returns:
        User: User object
    """
    avatar = avatar_gen(email)
    async with Prisma() as db:
        user = await db.user.create(data={'email': email, 'name':name, 'surname':surname, 'avatar':avatar}) #type: ignore
    return user

def avatar_gen(email):
    """Avatar Generation

    Args:
        email (str): User email

    Returns:
        str: Avatar URL
    """
    digest = md5(email.encode('utf-8')).hexdigest()
    return f'https://avatar.vercel.sh/{digest}?size=32'

async def user_activate(user_email, statut):
    """User Activation

    Args:
        user_email (str): User email
        statut (bool): User statut

    Returns:
        User: user object
    """
    async with Prisma() as db:
        user = await db.user.update(where={'email':user_email}, data={'active':statut})
    return user

async def user_optinNL(user, optinNL):
    """User Optin Nl

    Args:
        user (Obejct): User Object
        optinNL (bool): Optin Nl boolean

    Returns:
        User: User object
    """
    async with Prisma() as db:
        user = await db.user.update(where={'email':user.email}, data={'optinNL':optinNL, 'optinAt':datetime.now()}) #type: ignore
    return user

async def user_change_active_plan(customer, active_plan):
    async with Prisma() as db:
        user = await db.user.update(where={'id':customer.user_id}, data={'active_plan':active_plan})
    return user

async def user_change_plan(customer, plan):
    async with Prisma() as db:
        user = await db.user.update(where={'id':customer.user_id}, data={'plan':plan})
    return user

async def user_find_w_email(user_email):
    """User find with email

    Args:
        user_email (str): User email

    Returns:
        User: User Object
    """
    async with Prisma() as db:  
        user = await db.user.find_unique(where={'email': user_email})
    return user

async def user_email_update(user, user_new_email):
    """User update email

    Args:
        user (Object): User object
        user_new_email (str): User new email

    Returns:
        User: User object
    """
    avatar = avatar_gen(user_new_email)
    async with Prisma() as db:
        user = await db.user.update(where={'id': user.id}, data={'email':user_new_email, 'avatar':avatar})
    return user

async def user_update_data(user, data):
    """User update datas

    Args:
        user (Object): User object
        data (list): User new data list

    Returns:
        User: User object
    """
    async with Prisma() as db:
        user = await db.user.update(where={'email':user.email}, data={'name':data['name'], 'surname':data['surname']})
    return user

async def user_delete(user):
    """User delete

    Args:
        user (Object): User object

    Returns:
        User: User object
    """
    async with Prisma() as db:
        user = await db.user.delete(where={'user_id': user.user_id}) #type: ignore
    return user

async def user_get_all_data(user, include=None):
    include = include or []
    async with Prisma() as db:
        user = await db.user.find_unique(where={'id':user.id}, include={key: True for key in include}) # type: ignore
    return user