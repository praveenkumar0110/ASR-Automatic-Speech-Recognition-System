from django.db import models

class AudioTranscript(models.Model):
    audio_file = models.FileField(upload_to="audio/")
    transcript = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
