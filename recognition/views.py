from django.shortcuts import render
import traceback

from django.core.files.base import ContentFile, File

from .forms import UploadFileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import AudioFile, Chunks, TextFromAudio
from pydub import AudioSegment
import io
import os

from .tasks import transcribe_small_audio

@login_required(login_url='login_user')
def index(request):
    context = None
    audio_form = UploadFileForm()
    
    if request.method == "POST":
        # создаю форму
        audio_form = UploadFileForm(request.POST, request.FILES)
        
        if not audio_form.is_valid():
            messages.success(request, ("Error!"))
            return render(request, 'recognition/index.html', {"error": "Provide a valid file"})
        
        try:
            # save audio into database 
            form = audio_form.save(commit=False)
            form.user = request.user
            form.save()
            
            # take audio from db
            audio_object = AudioFile.objects.get(user=request.user)
            audio_file = audio_object.audio_file
            print(audio_file)
            
            # config            
            language = "ru-RU"
            minutes = 0.1
            
            # crush it into small chunks
            sound = AudioSegment.from_wav(audio_file.path)
            sound.set_frame_rate(16000).set_channels(1)
            chunk_length_ms = int(1000 * 60 * minutes)

            chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
            
            # save all my chunks into database
            save_chunks(chunks, request.user)

            
            # recognize our chunks
            try:
                
                transcribe_small_audio.delay(request.user.email)
                    

            except Exception:
                audio = AudioFile.objects.get(user = request.user)
                audio_files = Chunks.objects.filter(user=request.user).order_by("id")
                audio_files.delete()
                if audio:
                    audio.delete()
                    print(f"Exception occurred! Audio deleted!\n{Exception}")
                    raise Exception

            
        except Exception as ex: 
            traceback.print_exc()
        
            
            context = {"error": str(ex)}
    else:
        context = {
            "AudioForm" : audio_form
        }
    return render(request, "recognition/index.html", context )

def save_chunks(chunks, user):

    for i, audio_chunk in enumerate(chunks):
        buffer = io.BytesIO()
        audio_chunk.export(buffer, format="wav")
        buffer.seek(0)
        if buffer.getbuffer().nbytes == 0:
            raise ValueError(f"Chunk is empty, chunk--{i}")
        # take saved file
        chunk_file = File(buffer, name=f"{user.email}_chunk_{i}")
        # create a database object
        chunk_into_database = Chunks(user = user)
        # save file into object
        chunk_into_database.chunk.save(f"{user.email}_chunk_{i}", chunk_file)
        # save object into db
        chunk_into_database.save()
        print(f"Chunk {i} saved. User -- {user.email}")
    