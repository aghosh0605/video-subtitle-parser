from rest_framework import serializers
from .models import SubtitleDataModel,FileModel
from django.utils import timezone
import uuid

#Create your serializers here
class SubtitleDataSerializer(serializers.ModelSerializer):
    SubtitleID = serializers.CharField(required=False,default=str(uuid.uuid4()))
    start_time = serializers.CharField(max_length=15)
    end_time = serializers.CharField(max_length=15)
    subtitle = serializers.CharField(max_length=100)
    media_url = serializers.CharField(max_length=500,required=False)
    subtitle_url= serializers.CharField(max_length=500,required=False)
    modified_time = serializers.DateTimeField(required=False,default=timezone.now) #timezone Asis/Kolkata
    
    class Meta:
        model = SubtitleDataModel
        fields = ('__all__')
        
class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = FileModel
        fields = ('file', 'remark', 'timestamp')