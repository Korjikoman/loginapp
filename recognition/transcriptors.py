import os

from django.core.files.storage import default_storage
from django.conf import settings

import speech_recognition as sr
from pydub import AudioSegment

from asgiref.sync import async_to_sync, sync_to_async
from .models import TextFromAudio

r = sr.Recognizer()

def transcribe_small_audio(path, language):
    file = default_storage.open(path)
    with sr.AudioFile(file) as source:
        audio_data = r.record(source)
        text = str(r.recognize_google(audio_data, language=language))
    file.close()
    
    return text


async def get_large_audio_transcription(path,language,minutes=1):

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
            text = transcribe_small_audio(chunk_filename, language="ru-RU")
            
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}."
            print(text)
            whole_text += text
            text_model = TextFromAudio(text=text)
            await sync_to_async(text_model.save)()
            await sync_to_async(text_model.delete)()
            
    return whole_text
