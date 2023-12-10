from prisma import Prisma
import prisma

class MediaType:
    Video = 'Video'
    Picture = 'Picture'
    
class MediaFormat:
    Portrait = 'Portrait'
    Landscape = 'Landscape'
    
metadata_example = [
    {
        'prompt': '',
        'model': '',
        'description': '',
        'size': '',
    }
]

async def medias_create(name, media_type, media_format, metadata, collections):
    async with Prisma() as db:
        medias = await db.medias.create(data={'name':name, 'mediaType':media_type, 'mediaFormat':media_format, 'metadata':metadata,'collections_id':collections.id})
    return medias

async def medias_delete(medias):
    async with Prisma() as db:
        medias = await db.medias.delete(where={'id':medias.id})
    return medias
