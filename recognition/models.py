from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class AudioFile(models.Model):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    name = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    audio = models.FileField(upload_to='Audios/', null=True)
    file_type = models.CharField(max_length=5, blank=True)
    created = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField(null=True)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['name', 'created']
        verbose_name_plural = "Audio File Records"
    

    