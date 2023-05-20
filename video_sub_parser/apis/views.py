from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SubtitleDataModel,FileModel
from .serializers import SubtitleDataSerializer,FileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .dynamodb import DynamoServices
from celery.result import AsyncResult
from .tasks import uploads3
from django.conf import settings
from .extractor import *
import os
#For allowing CORS
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class VideoParse(APIView):
    _dbobj = DynamoServices()
    
    def post(self, request):
        serializer = SubtitleDataSerializer(data=request.data)
        
        if serializer.is_valid():
            # serializer.save()
            VideoParse._dbobj.createItem(serializer.data)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request,id=None):
        if id:
            res = AsyncResult(id)
            print(res.result)
            return Response({"status": "success", "data": 'hey'}, status=status.HTTP_200_OK)

        else:
            return Response({"status": "error", "data":"No task ID is given"}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    _dbobj = DynamoServices()
    
    def post(self, request):
        file_serializer = FileSerializer(data=request.data)
        
        if file_serializer.is_valid():
            # Saves file locally and generate the actual path
            file_serializer.save()
            save_path = os.path.join(settings.BASE_DIR, str(file_serializer.data['file']).strip("/"))

            # Uses the path to upload the file to s3 bucket
            if os.path.isfile(save_path):
                uploads3.delay(save_path)
                filename = os.path.basename(save_path)
                
            return Response(data={"filename":filename}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        search_query=self.request.query_params.get('query', None)
        if search_query:
            result = FileView._dbobj.searchItem(search_query)
            return Response(data=result, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":"No subtitle found"}, status=status.HTTP_400_BAD_REQUEST)
class FileParseView(APIView):
    
    def get(self,request,file=None):
        filename=self.request.query_params.get('file', None)

        if filename:
            save_path = os.path.join(settings.BASE_DIR, f'media/uploads/{filename}')
            # task_id = extractSubtitle(save_path)
            task_id = wait_sometime.delay(5)

            return Response(data={"message":"Started parsing video", "task_id":str(task_id)}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":"No video found"}, status=status.HTTP_400_BAD_REQUEST)