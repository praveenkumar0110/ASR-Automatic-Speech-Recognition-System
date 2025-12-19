# from django.urls import path
# from .views import upload_audio, get_all_transcripts

# urlpatterns = [
#     path("upload/", upload_audio),
#     path("all/", get_all_transcripts),
# ]



# from django.urls import path
# from .views import upload_audio, get_all_transcripts

# urlpatterns = [
#     path("upload/audio/", upload_audio),
#     path("all/", get_all_transcripts),
# ]

from django.urls import path
from .views import upload_audio, process_common_words

urlpatterns = [
    path("upload/audio/", upload_audio),
    path("process/common/", process_common_words),
]


