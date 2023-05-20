from celery_progress.backend import ProgressRecorder
from celery import shared_task 
from django.conf import settings
from celery_progress.backend import ProgressRecorder
from apis.utils.dynamodb import DynamoDBServices
import os
import uuid

_DBObj=DynamoDBServices()

@shared_task(bind=True)
def insertItems(self,subtitle_path,media_path):
    progress_recorder = ProgressRecorder(self)

    # Prepare variables
    s3_subtitle_url= os.path.join(settings.BUCKET_URL,f'subtitles/{os.path.basename(subtitle_path)}')
    s3_upload_url =os.path.join(settings.BUCKET_URL,f'uploads/{os.path.basename(media_path)}')
    data = []
    
    #Arrange the list of items to upload
    with open(subtitle_path) as f:
        for line in f:
            words = line.split('|')
            # print(words)
            dataItem={"SubtitleID": str(uuid.uuid4()),"start_time":words[0].strip(), "end_time":words[1].strip(),"subtitle":words[3].strip(), "media_path":s3_upload_url, "subtitle_url":s3_subtitle_url}
            data.append(dataItem)
            # print(json.dumps(data, indent=4))
    
    data_len = len(data)       
    print(f'\nTotal count of subtitles: {data_len}')
        
    #Insert the items one by one
    # For Single item
        # DynamoServices.__table.put_item(Item= data)
        
        #For multiple items use below
    with _DBObj.table.batch_writer() as batch:
            for item in data:
                response = batch.put_item(Item=item)
                progress_recorder.set_progress(data.index(item)+1, data_len,f'Insert Progress')
    print("Uploaded all items to DynamoDB")
    
    
    # Clean up all local files
    os.remove(subtitle_path)
    os.remove(media_path)
    print('Background DynamoDB Insert Completed')
    