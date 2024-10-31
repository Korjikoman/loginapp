from django.shortcuts import render

from .forms import UploadFileForm
import assemblyai as aai
from django.contrib import messages
import speech_recognition as sr
from pydub import AudioSegment
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .consumers import TranscriptionConsumer


r = sr.Recognizer()


def transcribe_small_audio(path, language):
    file = default_storage.open(path)
    with sr.AudioFile(file) as source:
        audio_data = r.record(source)
        text = str(r.recognize_google(audio_data, language=language))
    file.close()
    
    return text


def get_large_audio_transcription(path,language, consumer ,minutes=2):
    sound = AudioSegment.from_file(path)
    
    chunk_length_ms = int(1000*60*minutes)
    
    chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
    
    folder_name=str(settings.MEDIA_ROOT) + "/audio-chunks/"
    
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
        
    whole_text = ""
    
    for i, audio_chunk in enumerate(chunks,start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        
        try:
            text = transcribe_small_audio(chunk_filename, language)
            
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}."
            print(text)
            whole_text += text
            
            # Sending text through WebSocket
            consumer.send_text(text)
            
            # deleting chunk
            try:
                os.remove(chunk_filename)
            except FileNotFoundError:
                print("Error: file not found")
    return whole_text

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
            
            file_path = str(settings.MEDIA_ROOT) + '/' + str(file.name)
            if (file.size < 512000):
                text = transcribe_small_audio(file_path, language="en-US")
            
            else:
                consumer = TranscriptionConsumer()
                messages.success(request, ("File size is too big. We will give you a file with transcription..."))
                text = get_large_audio_transcription(file_path,"en-US", consumer)
            
            os.remove(file_path)
            
            context = {
                "text" :text,
                "AudioForm":audio_form,
                "file" : file
                }
            
        except Exception as ex:
            context = {"error": str(ex)}
    else:
        context = {
            "AudioForm" : audio_form
        }
    return render(request, "recognition/index.html", context )