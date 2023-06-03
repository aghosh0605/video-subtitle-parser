from django.db import models
from django.utils import timezone
import uuid
import os
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# add this to some file where you can import it from
def file_size(value): 
    limit = 100 * 1024 * 1024 #Max size can be 5 GB. Now it is 100MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 100 MB.')

# Create your models here.
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/', filename)


class FileModel(models.Model):
    file = models.FileField(upload_to=get_file_path,blank=False, null=False,validators=[FileExtensionValidator(allowed_extensions=['mp4','mkv','avi']),file_size])
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    
