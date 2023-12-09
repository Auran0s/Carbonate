from prisma import Prisma
import prisma

class MediaType:
    Video = 'Video'
    Picture = 'Picture'
    
class MediaFormat:
    Portrait = 'Portrait'
    Paysage = 'Landscape'

async def medias_create(name, media_type, media_format, url, metadata, collections):
    async with Prisma() as db:
        medias = await db.medias.create(data={'name':name, 'mediaType':media_type, 'mediaFormat':media_format, 'url':url, 'metadata':metadata, 'collections':{'connect':collections.id}})
    return medias

async def media_delete(medias):
    async with Prisma() as db:
        medias = await db.medias.delete(where={'id':medias.id})
    return medias