from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from apis.utils.dynamodb import DynamoDBServices
from .tasks import uploads3
from celery.result import AsyncResult
from django.conf import settings
from apis.utils.extractor import *
from apis.serializers import FileSerializer
import os
#For allowing CORS
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Initiate DynamoDB Cleint Object
_DBObj = DynamoDBServices()

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        file_serializer = FileSerializer(data=request.data)
        
        if file_serializer.is_valid():
            # Saves file locally and generate the actual path
            file_serializer.save()
            save_path = os.path.join(settings.BASE_DIR, str(file_serializer.data['file']).strip("/"))
            #print(save_path)
            
            # Uses the path to upload the file to s3 bucket
            if os.path.isfile(save_path):
                upload_id = uploads3.delay(save_path)
                filename = os.path.basename(save_path)
            return Response(data={"message":"Uploading the Video. Please wait ....","filename":filename, "task_id":str(upload_id)}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,file=None):
        filename=self.request.query_params.get('file', None)

        if filename:
            save_path = os.path.join(settings.BASE_DIR, f'media/uploads/{filename}')
            parse_id = extractSubtitle(save_path)

            return Response(data={"message":"Started Processing Video Subtitle", "task_id":str(parse_id)}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":"Please provide the video file name"}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class QueryView(APIView):
    
    def get(self,request):
        # Get Query from Request
        search_query=self.request.query_params.get('query', None)
        
        if search_query:
            result = _DBObj.searchItem(search_query.upper())
            return Response(data=result, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":"No subtitle found"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        if id:
            res = AsyncResult(id)
            return Response(data=res.ready(), status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":"No task found"}, status=status.HTTP_400_BAD_REQUEST)