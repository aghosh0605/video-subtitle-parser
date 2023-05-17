from django.db import models
from django.utils import timezone
# Create your models here.


class SubtitleDataModel(models.Model):
    start_time = models.CharField(max_length=15,blank=True, null=True)
    end_time = models.CharField(max_length=15,blank=True, null=True)
    subtitle = models.CharField(max_length=100,blank=True, null=True)
    modified_time = models.DateTimeField(default=timezone.now)
