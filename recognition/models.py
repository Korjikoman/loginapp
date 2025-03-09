from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from app.models import Users
class AudioFile(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    audio_file = models.FileField(upload_to='Audios/', null=True, validators=[FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'aac', 'flac', 'ogg'])])
    created = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField(null=True)
    
    language = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f'{self.user}'
    
    class Meta:
        ordering = ['created']
        verbose_name_plural = "Audio Files"
    

class TextFromAudio(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=1000)
    added = models.TimeField(default=timezone.now)
    
    def __str__(self):
        return self.text
    
class Chunks(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    chunk = models.FileField(upload_to="AudioChunks/",null=True, validators=[FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'aac', 'flac', 'ogg'])])
    uploaded = models.TimeField(default=timezone.now)
    
    def __str__(self):
        return f"chunk_{self.id}_{self.user}"