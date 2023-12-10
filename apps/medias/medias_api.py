from flask import Blueprint, redirect, request, url_for, session, flash, current_app
import firebase_admin
from firebase_admin import credentials, storage
import hashlib
from .medias_models import *
from apps.collections.collections_models import *
import os

medias_api = Blueprint('medias_api', __name__)

cred = credentials.Certificate("apps/medias/carbonate-a2fdc-firebase-adminsdk-e5vox-94c71de42f.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'carbonate-a2fdc.appspot.com'})

bucket = storage.bucket()


@medias_api.route('/api/medias/upload', methods=['POST']) # type: ignore
async def medias_api_upload_file():
    
    if 'file' not in request.files:
        return 'No file part', 500

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return 'No selected file'

    if uploaded_file:
        file_name = uploaded_file.filename
        
        collections = await collections_get('7402c65d-7142-4ea3-a13d-ae5b5f59e582')

        media = await medias_create(file_name, 'Video','Landscape', ['test'], collections)
        
        blob = bucket.blob(f"{media.id}.{file_name.split('.')[-1]}")
        blob.upload_from_file(uploaded_file, content_type='image/png')
        blob.make_public()
    

        return {'url': blob.public_url}, 200