from django.contrib import admin
from .models import AudioFile, TextFromAudio, Chunks
# Register your models here.
admin.site.register(AudioFile)
admin.site.register(TextFromAudio)
admin.site.register(Chunks)