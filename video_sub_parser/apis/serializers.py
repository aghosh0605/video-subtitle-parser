from rest_framework import serializers
from .models import FileModel
from django.utils import timezone
import uuid

#Create your serializers here
class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = FileModel
        fields = ('file', 'remark', 'timestamp')