from prisma import Prisma
import yaml

from prisma.enums import Plan

from apps.stripe.stripe_models import *

def restrictions_get():
    """Get restrictions for function

    Returns:
        List of restriction by function: 
    """
    with open("apps/restrictions/config/restrictions.yml", "r") as f:
        roles_restrictions = yaml.safe_load(f)
    return roles_restrictions

async def restrictions_init_uses(user):
    """Init restriction for an user

    Args:
        user (User Object): the user

    Returns:
        The uses Object
    """
    restrictions = restrictions_get()
    async with Prisma() as db:
        for function, use in restrictions['restrictionsPlan'][user.plan]:
            uses = await db.restrictions.create(data={
                'user_id':user.id,
                'function':function,
                'uses_number':0
            })
    return uses

async def restrictions_get_all_uses(user):
    """Get user restriction

    Args:
        user (User Object): the user

    Returns:
        The uses Object
    """
    async with Prisma() as db:
        uses = await db.restrictions.find_many(
            where={
                'user_id':user.id
            }
        )
    return uses

async def restrictions_get_use_w_function(function, user):
    """Get the user restriction from a function 

    Args:
        function (String): the name of the function
        user (User Object): the user

    Returns:
        use Object of this function
    """
    restrictions = restrictions_get()
    async with Prisma() as db:
        use = await db.restrictions.find_first(
            where={
                'AND':[
                    {'user_id':{'equals': user.id},},
                    {'function':{'equals': function}}
                ]
            }
        )
    return use, restrictions['restrictionsPlan'][user.plan][0][1]

async def restrictions_update_uses(function, user):
    """Update user restriction uses for a function after his uses

    Args:
        function (String): the name of the function
        user (User Object): the user

    Returns:
        JSON with the number of uses keep
    """
    restrictions = restrictions_get()
    
    use = await restrictions_get_use_w_function(function, user)
    
    if use.uses_number >= restrictions['restrictionsPlan'][user.plan][use.function]:
        return {'data': "You didn't have enought credits"}

    async with Prisma() as db:
        use = await db.restrictions.update(
            where={
            'id':use.id
            },
            data={
                'uses_number':{
                    'increment':restrictions['functions'][use.function]
                }
            }
        )
    return {'data':f'{use.uses_number}/10'}

async def restrictions_reset_uses(user):
    """Reset uses from an user

    Args:
        user (User Object): the user
    """
    restrictions = restrictions_get()
    async with Prisma() as db:
        for function, use in restrictions['restrictionsPlan'][user.plan]:
            uses = await db.restrictions.update_many(
                where={
                'AND':[
                    {'user_id':{'equals': user.id},},
                    {'function':{'equals': function}}
                ]
                },
                data={
                    'uses_number':use
                }
            )
    return uses  