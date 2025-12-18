from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")


db = client["audio_transcript_db"]


transcript_collection = db["transcripts"]
