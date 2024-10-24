from django.db import models

class AudioFile(models.Model):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    filename = models.CharField(max_length=100)
    file_type = models.Charfield(max_length=5, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(max_length=10)
    
    def __str__(self):
        return f'{self.filename}'
    
    class Meta:
        ordering = ['filename', 'created']
        verbose_name_plural = "Audio File Records"
    

    