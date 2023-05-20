from django.urls import path
from .views import FileView,QueryView

urlpatterns = [
    path('upload/file', FileView.as_view(), name='file-upload'),
    path('parse', FileView.as_view()),
    path('subtitle/find',QueryView.as_view()),
    path('status/file/<str:id>',QueryView.as_view())
]