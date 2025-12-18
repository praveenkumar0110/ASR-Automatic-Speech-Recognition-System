# import whisper
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from datetime import datetime

# from .db import transcript_collection


# model = whisper.load_model("base")

# @csrf_exempt
# def upload_audio(request):
   
#     if request.method != "POST":
#         return JsonResponse({
#             "message": "Use POST with audio file"
#         })

  
#     if "audio" not in request.FILES:
#         return JsonResponse({
#             "error": "Audio file not found"
#         }, status=400)

#     audio_file = request.FILES["audio"]

  
#     temp_path = f"media/{audio_file.name}"
#     with open(temp_path, "wb+") as f:
#         for chunk in audio_file.chunks():
#             f.write(chunk)

#    #text+ time
#     result = model.transcribe(temp_path)

   
#     transcript_text = []
#     for seg in result["segments"]:
#         transcript_text.append({
#             "start": round(seg["start"], 2),
#             "end": round(seg["end"], 2),
#             "text": seg["text"].strip()
#         })

   
#     document = {
#         "file_name": audio_file.name,
#         "created_at": datetime.utcnow(),
#         "language": result.get("language"),
#         "segments": transcript_text
#     }

#     inserted = transcript_collection.insert_one(document)

  
#     return JsonResponse({
#         "message": "Transcription successful",
#         "mongo_id": str(inserted.inserted_id),
#         "segments": transcript_text
#     })


# def get_all_transcripts(request):
#     data = []
#     for doc in transcript_collection.find():
#         data.append({
#             "id": str(doc["_id"]),
#             "file_name": doc["file_name"],
#             "created_at": doc["created_at"],
#             "segments": doc["segments"]
#         })

#     return JsonResponse(data, safe=False)



#all language model
import whisper
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .db import transcript_collection

# Load Whisper multilingual model
model = whisper.load_model("base")

@csrf_exempt
def upload_audio(request):

    if request.method != "POST":
        return JsonResponse({"message": "Use POST with audio file"}, status=405)

    if "audio" not in request.FILES:
        return JsonResponse({"error": "Audio file not found"}, status=400)

    audio_file = request.FILES["audio"]

    # Save audio temporarily
    temp_path = f"media/{audio_file.name}"
    with open(temp_path, "wb+") as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    # 🔥 Auto language detection (ALL languages)
    result = model.transcribe(
        temp_path,
        task="transcribe"
    )

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": round(seg["start"], 3),  # seconds + milliseconds
            "end": round(seg["end"], 3),
            "text": seg["text"].strip()
        })

    document = {
        "file_name": audio_file.name,
        "created_at": datetime.utcnow(),
        "language": result["language"],
        "segments": segments
    }

    inserted = transcript_collection.insert_one(document)

    return JsonResponse({
        "message": "Transcription successful",
        "language": result["language"],
        "mongo_id": str(inserted.inserted_id),
        "segments": segments
    })


def get_all_transcripts(request):
    data = []

    for doc in transcript_collection.find():
        data.append({
            "id": str(doc["_id"]),
            "file_name": doc["file_name"],
            "created_at": doc["created_at"],
            "language": doc.get("language"),
            "segments": doc["segments"]
        })

    return JsonResponse(data, safe=False)
