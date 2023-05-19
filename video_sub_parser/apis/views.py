from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SubtitleDataModel,FileModel
from .serializers import SubtitleDataSerializer,FileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .dynamodb import DynamoServices
#For allowing CORS
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .s3 import upload_file
from django.conf import settings
from .extractor import *
import os

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
            item = SubtitleDataModel.objects.get(id=id)
            serializer = SubtitleDataSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = SubtitleDataModel.objects.all()
        serializer = SubtitleDataSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    _dbobj = DynamoServices()
    
    def post(self, request):
        file_serializer = FileSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            save_path = os.path.join(settings.BASE_DIR, str(file_serializer.data['file']).strip("/"))
            # print(save_path)
            if os.path.isfile(save_path):
                upload_file(save_path)
                # os.remove(save_path)
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
        # print(filename)
        if filename:
            save_path = os.path.join(settings.BASE_DIR, f'media/uploads/{filename}')
            extractSubtitle(save_path)
            return Response(data={"message":"Parsed Video"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":"No video found"}, status=status.HTTP_400_BAD_REQUEST)