from pymongo import MongoClient

# Mongo connection
client = MongoClient("mongodb://localhost:27017")

# Database
db = client["audio_transcript_db"]

# Collection
transcript_collection = db["transcripts"]
