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



# #all language model
# import whisper
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from datetime import datetime

# from .db import transcript_collection


# model = whisper.load_model("base")

# @csrf_exempt
# def upload_audio(request):

#     if request.method != "POST":
#         return JsonResponse({"message": "Use POST with audio file"}, status=405)

#     if "audio" not in request.FILES:
#         return JsonResponse({"error": "Audio file not found"}, status=400)

#     audio_file = request.FILES["audio"]


#     temp_path = f"media/{audio_file.name}"
#     with open(temp_path, "wb+") as f:
#         for chunk in audio_file.chunks():
#             f.write(chunk)

  
#     result = model.transcribe(
#         temp_path,
#         task="transcribe"
#     )

#     segments = []
#     for seg in result["segments"]:
#         segments.append({
#             "start": round(seg["start"], 3),  
#             "end": round(seg["end"], 3),
#             "text": seg["text"].strip()
#         })

#     document = {
#         "file_name": audio_file.name,
#         "created_at": datetime.utcnow(),
#         "language": result["language"],
#         "segments": segments
#     }

#     inserted = transcript_collection.insert_one(document)

#     return JsonResponse({
#         "message": "Transcription successful",
#         "language": result["language"], 
#         "mongo_id": str(inserted.inserted_id),
#         "segments": segments
#     })


# def get_all_transcripts(request):
#     data = []

#     for doc in transcript_collection.find():
#         data.append({
#             "id": str(doc["_id"]),
#             "file_name": doc["file_name"],
#             "created_at": doc["created_at"],
#             "language": doc.get("language"),
#             "segments": doc["segments"]
#         })

#     return JsonResponse(data, safe=False)

import whisper
import re
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pydub import AudioSegment
from bson import ObjectId

from .db import transcript_collection


# =========================================
# Load Whisper model ONCE
# =========================================
model = whisper.load_model("base")


# =========================================
# Helper functions
# =========================================

def clean_words(text):
    """
    punctuation remove pannum
    lowercase pannum
    words split pannum
    """
    return re.sub(r"[^\w\s]", "", text.lower()).split()


def read_template_words(path):
    """
    sample1.txt read pannum
    """
    with open(path, "r", encoding="utf-8") as f:
        return clean_words(f.read())


def get_common_words(template_words, segment_text):
    """
    template text vs transcript segment
    common words mattum return pannum
    """
    segment_words = set(clean_words(segment_text))
    return [w for w in template_words if w in segment_words]


def word_level_time(start, end, words):
    """
    segment time-a equal-aa split panni
    word-by-word timestamp create pannum
    """
    if not words:
        return []

    duration = end - start
    step = duration / len(words)

    result = []
    for i, word in enumerate(words):
        w_start = round(start + i * step, 3)
        w_end = round(w_start + step, 3)
        result.append({
            "word": word,
            "start": w_start,
            "end": w_end
        })

    return result


def save_common_txt(words, path):
    """
    common_words.txt create pannum
    """
    with open(path, "w", encoding="utf-8") as f:
        for w in words:
            f.write(f"{w['word']}\t{w['start']} → {w['end']}\n")


def cut_audio(audio_path, words, output_path):
    """
    common words audio mattum cut pannum
    """
    audio = AudioSegment.from_file(audio_path)
    final_audio = AudioSegment.empty()

    for w in words:
        start_ms = int(w["start"] * 1000)
        end_ms = int(w["end"] * 1000)
        final_audio += audio[start_ms:end_ms]

    final_audio.export(output_path, format="ogg")


# ======================================================
# API 1️⃣ : Upload audio → TRANSCRIPT with timestamp
# URL : POST /api/upload/audio/
# ======================================================
@csrf_exempt
def upload_audio(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST method only"}, status=405)

    if "audio" not in request.FILES:
        return JsonResponse({"error": "Audio file required"}, status=400)

    audio_file = request.FILES["audio"]
    audio_path = f"media/{audio_file.name}"

    # save audio
    with open(audio_path, "wb+") as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    # Whisper transcription
    result = model.transcribe(audio_path, task="transcribe")

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": round(seg["start"], 3),
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
        "message": "Transcript created successfully",
        "transcript_id": str(inserted.inserted_id),
        "segments": segments
    })


# ======================================================
# API 2️⃣ : Compare transcript + sample1.txt
# Create text + cut audio
# URL : POST /api/process/common/
# ======================================================
@csrf_exempt
def process_common_words(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST method only"}, status=405)

    transcript_id = request.POST.get("transcript_id")
    audio_file = request.FILES.get("audio")

    if not transcript_id or not audio_file:
        return JsonResponse(
            {"error": "transcript_id and audio required"},
            status=400
        )

    # save audio again (same audio)
    audio_path = f"media/{audio_file.name}"
    with open(audio_path, "wb+") as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    # get transcript from MongoDB
    try:
        transcript = transcript_collection.find_one(
            {"_id": ObjectId(transcript_id)}
        )
    except:
        return JsonResponse({"error": "Invalid transcript_id"}, status=400)

    if not transcript:
        return JsonResponse({"error": "Transcript not found"}, status=404)

    # read template text
    template_words = read_template_words("media/sample1.txt")

    all_word_times = []

    for seg in transcript["segments"]:
        common_words = get_common_words(
            template_words,
            seg["text"]
        )

        times = word_level_time(
            seg["start"],
            seg["end"],
            common_words
        )

        all_word_times.extend(times)

    # output files
    txt_output = "media/common_words.txt"
    audio_output = "media/common_words_audio.ogg"

    save_common_txt(all_word_times, txt_output)
    cut_audio(audio_path, all_word_times, audio_output)

    return JsonResponse({
        "message": "Common words processed successfully",
        "common_words_count": len(all_word_times),
        "text_file": txt_output,
        "audio_file": audio_output
    })
