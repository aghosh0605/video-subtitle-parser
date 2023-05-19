from django.urls import path
from .views import VideoParse,FileView,FileParseView

urlpatterns = [
    path('subtitle', VideoParse.as_view()),
    path('subtitle/<int:id>', VideoParse.as_view()),
    path('upload', FileView.as_view(), name='file-upload'),
    path('parse', FileParseView.as_view()),
]