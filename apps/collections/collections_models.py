from prisma import Prisma

async def collections_create(name, users):
    async with Prisma() as db:
        collections = await db.collections.create(data={'name':name, 'users':{'connect':[{'id':user.id} for user in users]}})
    return collections

async def collections_add_media(collections, medias):
    async with Prisma() as db:
        collections = await db.collections.update(where={'id':collections.id}, data={'medias':{'connect':[{'id':media.id} for media in medias]}})
    return collections

async def collections_delete_media(collections, medias):
    async with Prisma() as db:
            collections = await db.collections.update(where={'id':collections.id}, data={'medias':{'disconnect':[{'id':media.id} for media in medias]}})
    return collections

async def collections_get(collections):
    async with Prisma() as db:
        collections = await db.collections.find_unique(where={'id':collections.id})
    return collections

async def collections_get_medias(collections):
    async with Prisma() as db:
        collections = await db.collections.find_unique(where={'id':collections.id}, include={'medias': True})
    return collections

async def collections_get_users(collections):
    async with Prisma() as db:
        collections = await db.collections.find_unique(where={'id':collections.id}, include={'users': True})
    return collections

async def collections_update_name(collections, name):
    async with Prisma() as db:
        collections = await db.collections.update(where={'id':collections.id}, data={'name':name})
    return collections

async def collections_add_users(collections, users):
    async with Prisma() as db:
        collections = await db.collections.update(where={'id':collections.id}, data={'users':{'connect':[{'id':user.id} for user in users]}})
    return collections

async def collections_delete(collections):
    async with Prisma() as db:
        collections = await db.collections.delete(where={'id':collections.id})
    return collections