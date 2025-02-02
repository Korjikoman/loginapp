from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from app.models import Users
class AudioFile(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    audio_file = models.FileField(upload_to='Audios/', null=True, validators=[FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'aac', 'flac', 'ogg'])])
    file_type = models.CharField(max_length=5, blank=True)
    created = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField(null=True)
    text_file = models.FileField(null=True)
    
    
    def __str__(self):
        return f'{self.user}'
    
    class Meta:
        ordering = ['created']
        verbose_name_plural = "Audio Files"
    

class TextFromAudio(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text
    