# 🎙️ ASR – Automatic Speech Recognition System (Django + Whisper)

A **Django-based Automatic Speech Recognition (ASR) backend** built using **OpenAI Whisper** to convert clear audio into **high-accuracy, word-by-word transcripts with timestamps (seconds & milliseconds)**.  
The system exposes **REST APIs**, supports **language detection**, stores results in **MongoDB**, and performs **accuracy analysis** for speech evaluation and subtitle generation.

---

## 🚀 Features

### ✅ Speech-to-Text
- Converts audio files into accurate text
- Powered by **OpenAI Whisper**
- Automatic language detection
- Optimized for clear audio input

### ⏱️ Word-by-Word Timestamps
- Timestamp for **every word**
- Precision in **seconds and milliseconds**
- Ideal for:
  - Subtitles (SRT / VTT)
  - Speech evaluation
  - Audio-text alignment

### 📊 Accuracy Analysis
- Compares ASR output with reference text
- Detects:
  - Missing words
  - Extra words
  - Incorrect words
- Useful for evaluation and benchmarking

### 🗄️ MongoDB Storage
- Stores:
  - Audio metadata
  - Full transcripts
  - Word-level timestamps
  - Accuracy results

### 🌐 REST APIs
- Built using **Django REST Framework**
- Easy frontend and mobile integration

---

## 🛠️ Tech Stack

| Component | Technology |
|--------|-----------|
| Backend | Django, Django REST Framework |
| ASR Model | OpenAI Whisper |
| Audio Processing | FFmpeg, PyDub, SoundFile |
| Database | MongoDB |
| ML | PyTorch, Torchaudio |
| Language | Python 3.9+ |

---

## 📂 Project Structure

ASR-Automatic-Speech-Recognition-System/
│
├── server/ # Django project settings
├── transcript/ # ASR & transcript logic
│ ├── views.py
│ ├── urls.py
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore

yaml
Copy code

---

## ⚙️ Installation & Setup
### 1️⃣ Clone Repository
```bash
git clone https://github.com/praveenkumar0110/ASR-Automatic-Speech-Recognition-System-V3.git
cd ASR-Automatic-Speech-Recognition-System
