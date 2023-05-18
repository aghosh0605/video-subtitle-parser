from django.db import models
from django.utils import timezone
import uuid
# Create your models here.


class SubtitleDataModel(models.Model):
    SubtitleID = models.CharField(max_length=36, default=str(uuid.uuid1()))
    start_time = models.CharField(max_length=15,blank=True, null=True)
    end_time = models.CharField(max_length=15,blank=True, null=True)
    subtitle = models.CharField(max_length=100,blank=True, null=True)
    modified_time = models.DateTimeField(default=timezone.now) #timezone Asis/Kolkata
