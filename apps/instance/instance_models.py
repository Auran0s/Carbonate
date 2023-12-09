from prisma import Prisma

async def instance_create(user):
    """Instance creation

    Args:
        user (User): User Object

    Returns:
        Instance: Instance object
    """
    async with Prisma() as db:
        instance = await db.instances.create(data={'user_id':user.id})
    return instance

async def instance_delete(instance_id):
    async with Prisma() as db:
        instance = await db.instances.delete(where={'id':instance_id})
    return instance

async def instance_find_all(user):
    async with Prisma() as db:
        instance = await db.user.find_unique(where={'id':user.id}, include={'instances':True})
    return instance

async def instance_find_w_api_key(instance_api_key):
    async with Prisma() as db:
        instance = await db.instances.find_unique(where={'apiKey': instance_api_key}, include={'credentials':True})
    return instance
