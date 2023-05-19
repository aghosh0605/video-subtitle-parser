import subprocess
from django.conf import settings
import os
import uuid
from .s3 import upload_file
from .dynamodb import DynamoServices
import json

_dbobj = DynamoServices()

def uploadSubtitle(subtitle_path,media_url):
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
        # _dbobj.createItem(data_to_upload)

def extractSubtitle(video_path):
    filename = uuid.uuid1()
    subtitle_path = os.path.join(settings.BASE_DIR,f'media/subtitles/{filename}.txt')
    # print(save_path)
    
    if os.path.isfile(video_path):
        cmd = f"ccextractor {video_path} -out=ttxt -o {subtitle_path}"
    # returns output as byte string
        returned_output = subprocess.check_output(cmd,shell=True)
    # using decode() function to convert byte string to string
    # print(returned_output.decode("utf-8"))
    
    if os.path.isfile(subtitle_path):
        upload_file(subtitle_path)
        uploadSubtitle(subtitle_path,video_path)
        # os.remove(video_path)
        os.remove(subtitle_path)