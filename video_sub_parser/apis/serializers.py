from rest_framework import serializers
from .models import SubtitleDataModel

#Create your serializers here
class SubtitleDataSerializer(serializers.ModelSerializer):
    start_time = serializers.CharField(max_length=15)
    end_time = serializers.CharField(max_length=15)
    subtitle = serializers.CharField(max_length=100)
    modified_time = serializers.DateTimeField(required=False)
    
    class Meta:
        model = SubtitleDataModel
        fields = ('__all__')