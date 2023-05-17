from django.urls import path
from .views import VideoParse

urlpatterns = [
    path('subtitle', VideoParse.as_view()),
    path('subtitle/<int:id>', VideoParse.as_view()),
]