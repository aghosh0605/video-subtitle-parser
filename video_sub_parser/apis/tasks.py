from celery import shared_task
import time
import os
from .dynamodb import DynamoServices
from django.conf import settings
import uuid
import json

_dbobj=DynamoServices()

@shared_task
def puItems(subtitle_path,media_url):
    
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
    print('Insert background task completed')