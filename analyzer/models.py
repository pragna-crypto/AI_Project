from django.db import models

class SpeechAnalysis(models.Model):
    title = models.CharField(max_length=200, default="Untitled Speech")
    audio_file = models.FileField(upload_to='speeches/')
    
    # Analysis metrics
    speech_speed_wpm = models.FloatField(null=True, blank=True)
    filler_words_count = models.IntegerField(null=True, blank=True)
    pause_count = models.IntegerField(null=True, blank=True)
    voice_volume_stability = models.FloatField(null=True, blank=True)
    
    # Scores
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Explanations
    speed_score = models.FloatField(null=True, blank=True)
    filler_score = models.FloatField(null=True, blank=True)
    pause_score = models.FloatField(null=True, blank=True)
    stability_score = models.FloatField(null=True, blank=True)
    
    transcript = models.TextField(null=True, blank=True)
    suggestions = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
