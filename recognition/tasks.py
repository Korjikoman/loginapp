import os
import speech_recognition as sr
from pydub import AudioSegment
from asgiref.sync import async_to_sync, sync_to_async
from .models import TextFromAudio,AudioFile, Chunks
import io
from django.core.files.base import ContentFile, File

import time
import whisper
import eventlet 

from .celery import app
from app.models import Users



r = sr.Recognizer()

@app.task(bind=True)
def from_mp3_to_wav(self):
    sound = AudioSegment.from_mp3(self.file_path)
    sound.export(self.file_path, format="wav")
    return self.file_path

@app.task()
def transcribe_small_audio(email):
    user = Users.objects.get(email=email)
    r = sr.Recognizer()
    model = whisper.load_model("turbo")
    
    
    audio_files = Chunks.objects.filter(user=user).order_by("id")
    for audio_file in audio_files:
        path = audio_file.chunk.path
        print(path)
    
    
        # распознаем текст
        with sr.AudioFile(path) as source:
            audio_data = r.record(source)
            start = time.time()
            try:
                result = model.transcribe(path, language="ru", fp16=False, verbose=True)            
                #text = r.recognize_whisper(audio_data)
                text = result["text"]
                print(f"{user.email} -- {user.id} Text has been transcribed, time: {time.time() - start:.2f} seconds")
            except sr.UnknownValueError:
                print("Speech was not recognized.")
                text = ""
            except sr.RequestError as e:
                print(f"API request failed: {e}")
                text = ""
        text_model = TextFromAudio(text=text, user = user)
        text_model.save()
    
    
    return text


    
    # def get_large_audio_transcription(self):
    #     try:
    #         sound = AudioSegment.from_wav(self.file_path)
    #         sound.set_frame_rate(16000).set_channels(1)
    #         chunk_length_ms = int(1000 * 60 * self.minutes)

    #         chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
            
    #         print(chunks)
    #         folder_name = "audio-chunks/"

    #         if not os.path.isdir(folder_name):
    #             os.mkdir(folder_name)
    #         print("DIVE INTO FUNCTION")
    #         self.save_chunks(chunks, folder_name)
    #             # try:
    #             #     text = self.transcribe_small_audio(chunk.audio_file.path)

    #             # except sr.UnknownValueError as e:
    #             #     print("Error:", str(e))
    #             # else:
    #             #     text = f"{text.capitalize()}."
    #             #     print("HUI")
    #             #     text_model = TextFromAudio(text=text, user = self.user)
    #             #     text_model.save()
    #     except Exception as e:
    #         audio = AudioFile.objects.get(user = self.user)
    #         if audio:
    #             audio.delete()
    #             print("Exception occurred! Audio deleted!")
    #         raise e
    
            
            

