# 🎙️ Audio Transcription API  
### Django + Whisper + MongoDB

<p align="center">
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/django/django.png" width="90"/>
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/python/python.png" width="90"/>
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/mongodb/mongodb.png" width="90"/>
</p>

A backend project that allows users to **upload audio files**, automatically **detect language**, convert **speech to text** using **OpenAI Whisper**, and store **timestamped transcription data** in **MongoDB**.

---

## 📌 Project Overview

<p align="center">
 
</p>

This project exposes REST APIs that:
- Accept audio files
- Transcribe speech into text
- Detect spoken language automatically
- Store transcription with timestamps
- Return structured JSON output

---

## 🔄 Workflow (How It Works)

<p align="center">
  
</p>

1. Client uploads an audio file via API  
2. Audio is saved temporarily on the server  
3. Whisper model processes the audio  
4. Language is auto-detected  
5. Speech is converted into text segments  
6. Each segment includes start & end timestamps  
7. Data is stored in MongoDB  
8. API returns transcription response  

---

## ✨ Features

- 🎧 Audio upload via REST API  
- 🌍 Multilingual support (auto language detection)  
- 📝 Speech-to-text using Whisper  
- ⏱️ Timestamped segments  
- 🗄️ MongoDB storage  
- 📄 Fetch all transcripts API  

---

## 🛠️ Tech Stack

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/75/Django_logo.svg" width="120"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="80"/>
  <img src="https://www.vectorlogo.zone/logos/mongodb/mongodb-icon.svg" width="80"/>
</p>

- **Backend:** Django  
- **Language:** Python  
- **Speech Model:** OpenAI Whisper  
- **Database:** MongoDB (PyMongo)  
- **Audio Tool:** FFmpeg  

---

## 📂 Project Structure

audio-transcription-api/
│
├── text/
│ ├── views.py # Upload & transcription logic
│ ├── urls.py # API routes
│ ├── db.py # MongoDB connection
│ └── models.py # Django model (future use)
│
├── media/
│ └── audio/ # Uploaded audio files
│
├── project/
│ └── urls.py # Main URL config
│
├── manage.py
└── README.md