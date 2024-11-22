from django.shortcuts import render
import traceback

from .forms import UploadFileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import transcriptors
import os

from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings


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
            form = audio_form.save(commit=False)
            form.name = request.user
            form.save()
            
            
            file = form.audio # get the audio 
            file_size = file.size
            file_path = str(settings.MEDIA_ROOT) + '/' + str(file.name)
            
            messages.success(request, ("File size is too big. We will give you a file with transcription..."))
            text = async_to_sync(transcriptors.get_large_audio_transcription)(file_path,"ru-RU")
            
            
            os.remove(file_path)
            
            context = {
                "text" :text,
                "AudioForm":audio_form,
                "size" : file_size
                }
            
        except Exception as ex: 
            traceback.print_exc()
            context = {"error": str(ex)}
    else:
        context = {
            "AudioForm" : audio_form 
        }
    return render(request, "recognition/index.html", context )