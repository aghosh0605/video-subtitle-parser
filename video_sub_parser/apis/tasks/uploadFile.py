from celery import shared_task
import os
from apis.utils.s3 import *

@shared_task(bind=True)
def uploads3(self,file_name,bucket=None,object_name=None):
    # If S3 object_name was not specified, use file_name to generate
    print(file_name)
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