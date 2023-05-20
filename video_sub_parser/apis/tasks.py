from celery import shared_task 
import os
from .dynamodb import DynamoServices
from .s3 import upload_file
from django.conf import settings
import uuid
import json
import time
from celery_progress.backend import ProgressRecorder

_dbobj=DynamoServices()

@shared_task(bind=True)
def puItems(self,subtitle_path,media_url):

    s3_subtitle_url= os.path.join(settings.BUCKET_URL,f'subtitles/{os.path.basename(subtitle_path)}')
    s3_upload_url =os.path.join(settings.BUCKET_URL,f'uploads/{os.path.basename(media_url)}')
    data_to_upload = []
    
    with open(subtitle_path) as f:
        for line in f:
            words = line.split('|')
            # print(words)
            data={"SubtitleID": str(uuid.uuid4()),"start_time":words[0].strip(), "end_time":words[1].strip(),"subtitle":words[3].strip(), "media_url":s3_upload_url, "subtitle_url":s3_subtitle_url}
            data_to_upload.append(data)
            # print(json.dumps(data, indent=4))
            
        print(f'\n=======>Total count of subtitles: {len(data_to_upload)}')
    _dbobj.createItem(data_to_upload)
    os.remove(subtitle_path)
    # os.remove(video_path)
    print('Insert background task completed')
    
    
@shared_task(bind=True)
def uploads3(file_name,bucket=None,object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        ext = os.path.splitext(file_name)[-1].lower()

        # Creates folder in bucket to upload files
        if ext == '.txt':
            object_name =  'subtitles/'+ os.path.basename(file_name)
        else:
            object_name = 'uploads/' + os.path.basename(file_name)
    
    # Bucket Name for upload
    if bucket is None:
        bucket = 'ecowiser-internship'
    
    # s3 client for uploading files
    upload_file(file_name,bucket,object_name)