from prisma import Prisma
import yaml

def credentials_services_list():
    with open("apps/credentials/services/services.yml", "r") as f:
        services_listing = yaml.safe_load(f)
    return services_listing['Services']

async def credentials_create_oauth2(name, token_type, access_token, refresh_token, expires_at, instance):
    """Create an Oauth creadentials

    Args:
        name (String): The name of the credentials
        token_type (String): the type of the token, returning by Notion endpoint
        access_token (String): The access token, returning by Notion endpoint
        refresh_token (String): The refresh token, returning by Notion endpoint
        expires_at (Timestamp): The date of the expiration of the refresh token, returning by Notion endpoint
        user (User Object): The user

    Returns:
        credentials: the new credential data's
    """
    async with Prisma() as db:
        credentials = await db.credentialsoauth2.create(
            data={
                'name':name,
                'token_type':token_type,
                'access_token':access_token,
                'refresh_token':refresh_token,
                'expires_at':expires_at,
                'instanceId':instance.id
        })
    return credentials

async def credentials_update_oauth2(credential, data):
    """Update Oauth credentials

    Args:
        credential (Credential Object): the credential who need to be updated
        data (Dict): The dict of the new data

    Returns:
        credentials: the credential object
    """
    async with Prisma() as db:
       credentials = await db.credentialsoauth2.update(
        where={
            'id':credential.id
        },
            data={
                'name':data['name'],
                'token_type':data['token_type'],
                'access_token':data['access_token'],
                'refresh_token':data['refresh_token'],
                'expires_at':data['expires_at'],
                'user_id':data['user.id']
        })
    return credentials 

async def credentials_find_w_instance(instance, name):
    """Find credential with an user

    Args:
        user (User Object): the user
        name (String): the name of the credential

    Returns:
        Object: the credential object
    """
    async with Prisma() as db:
        credentials = await db.credentialsoauth2.find_first(
            where={
                'instanceId':instance.id,
                'name':name
            }
        )
    return credentials

async def credentials_list_by_instance(instance):
    """Find credential with an user

    Args:
        user (User Object): the user
        name (String): the name of the credential

    Returns:
        Object: the credential object
    """
    async with Prisma() as db:
        credentials = await db.credentialsoauth2.find_many(
            where={
                'instanceId':instance.id,
            }
        )
    return credentials

async def credentials_delete(credential_id):
    async with Prisma() as db:
        credentials = await db.credentialsoauth2.delete(
            where={
                'id':credential_id
            }
        )
    return credentials