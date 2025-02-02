from django.shortcuts import render
import traceback

from .forms import UploadFileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .transcriptors import AudioToText
import os

from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from .models import AudioFile

@login_required(login_url='login_user')
def index(request):
    context = None
    audio_form = UploadFileForm()
    
    if request.method == "POST":
        audio_form = UploadFileForm(request.POST, request.FILES)
        
        if not audio_form.is_valid():
            messages.success(request, ("Error!"))
            return render(request, 'recognition/index.html', {"error": "Provide a valid file"})
        
        try:
            audioFileObjects = AudioFile.objects.all()
            print(audioFileObjects)
            
            form = audio_form.save(commit=False)
            form.user = request.user
            form.save()
            
            audioFileObjects = AudioFile.objects.all()
            print(audioFileObjects)
            
            file = form.audio_file # get the audio
            file_name, file_extension = os.path.splitext(file.name)
            file_path = str(settings.MEDIA_ROOT) + '/' + str(file.name)
            
            transcriptor = AudioToText(request.user,file_path, "ru-Ru", 0.15)
            if file_extension != ".wav":
                transcriptor.from_mp3_to_wav()
            
            # Большой файл >= 200 Mb
            if file.size >= 1677721600:
                messages.success(request, ("File size is too big. We will give you a file with transcription..."))
            
            text = async_to_sync(transcriptor.get_large_audio_transcription)()

            audioFile = audioFileObjects.filter(user=request.user)
            audioFile.delete()
            
            context = {
                    
                    "text" :text,
                    "AudioForm":audio_form,
                    "size" : file.size,
                    }
            
        except Exception as ex: 
            traceback.print_exc()
            context = {"error": str(ex)}
    else:
        context = {
            "AudioForm" : audio_form
        }
    return render(request, "recognition/index.html", context )