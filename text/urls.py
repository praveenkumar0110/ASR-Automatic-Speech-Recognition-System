from django.urls import path
from .views import upload_audio, get_all_transcripts

urlpatterns = [
    path("upload/", upload_audio),
    path("all/", get_all_transcripts),
]
