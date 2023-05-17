from django.urls import path
from .views import VideoParse,VideoParseSpecific

urlpatterns = [
    path('subtitle', VideoParse.as_view()),
    path('subtitle/<int:item_id>', VideoParseSpecific.as_view()),
]