from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from .models import SubtitleData
#For allowing CORS
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class VideoParse(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        subtitle = data.get('subtitle')

        subtitle_data = {
            'start_time': start_time,
            'end_time': end_time,
            'subtitle': subtitle,
        }

        subtitle_item = SubtitleData.objects.create(**subtitle_data)

        data = {"message":f"Data received at {subtitle_item.modified_time}"}
        return JsonResponse(data, status=201)
    
    
    def get(self, request):
        items_count = SubtitleData.objects.count()
        items = SubtitleData.objects.all()

        items_data = []
        for item in items:
            items_data.append({
                'start_time': item.start_time,
                'end_time': item.end_time,
                'subtitle': item.subtitle,
                'modified_time':item.modified_time
            })

        data = {
            'items': items_data,
            'count': items_count,
        }

        return JsonResponse(data)
    
@method_decorator(csrf_exempt, name='dispatch')
class VideoParseSpecific(View):
    def get(self, request, item_id):
        # data = json.loads(request.body.decode("utf-8"))
        item = SubtitleData.objects.get(id=item_id)
        # item.product_quantity = data['product_quantity']
        # item.save()
        
        data = {
            'item': subtitle_item,
            'count': 1,
        }

        return JsonResponse(data)