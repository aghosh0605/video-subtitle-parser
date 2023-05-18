from django.db import models
from django.utils import timezone
import uuid
import os

# Create your models here.
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/', filename)


class SubtitleDataModel(models.Model):
    SubtitleID = models.CharField(max_length=36, default=str(uuid.uuid1()))
    start_time = models.CharField(max_length=15,blank=True, null=True)
    end_time = models.CharField(max_length=15,blank=True, null=True)
    subtitle = models.CharField(max_length=100,blank=True, null=True)
    modified_time = models.DateTimeField(default=timezone.now) #timezone Asis/Kolkata


class FileModel(models.Model):
    file = models.FileField(upload_to=get_file_path,blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)