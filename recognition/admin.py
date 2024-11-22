from django.contrib import admin
from .models import AudioFile, TextFromAudio
# Register your models here.
admin.site.register(AudioFile)
admin.site.register(TextFromAudio)