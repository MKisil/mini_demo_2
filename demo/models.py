from django.db import models


class CallsAnalysis(models.Model):
    audio_file = models.FileField(upload_to='audio_files/')
    analysis_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
