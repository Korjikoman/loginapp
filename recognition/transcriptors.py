import os

from django.core.files.storage import default_storage
from django.conf import settings

import speech_recognition as sr
from pydub import AudioSegment

from asgiref.sync import async_to_sync, sync_to_async
from .models import TextFromAudio,AudioFile


r = sr.Recognizer()

import time
import whisper
    
# Добавление текста в вордовский файл
#from docx import Document


class AudioToText():
    def __init__(self, path_to_audio, language, minutes):

        self.file_path = path_to_audio
        self.lang = language
        self.minutes = minutes
        self.model = whisper.load_model("turbo")

    def from_mp3_to_wav(self):
        sound = AudioSegment.from_mp3(self.file_path)
        sound.export(self.file_path, format="wav")
        return self.file_path

    def transcribe_small_audio(self, path):
        r = sr.Recognizer()
        # распознаем текст
        with sr.AudioFile(path) as source:
            audio_data = r.record(source)
            start = time.time()
            try:
                result = self.model.transcribe(path, language="ru", fp16=False, verbose=True)            
                #text = r.recognize_whisper(audio_data)
                text = result["text"]
                print(f"Text has been transcribed, time: {time.time() - start:.2f} seconds")
            except sr.UnknownValueError:
                print("Speech was not recognized.")
                text = ""
            except sr.RequestError as e:
                print(f"API request failed: {e}")
                text = ""
        #удаляем чанк
        os.remove(path)
        
        return text

    async def get_large_audio_transcription(self):
        sound = AudioSegment.from_wav(self.file_path)
        sound.set_frame_rate(16000).set_channels(1)

        chunk_length_ms = int(1000 * 60 * self.minutes)

        chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]

        folder_name = "audio-chunks/"

        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        whole_text = ""

        file = open('text.txt', 'w')
        
        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")

            try:
                text = self.transcribe_small_audio(chunk_filename)
                file.write(text)

            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}."
                print(text)
                whole_text += text
                text_model = TextFromAudio(text=text)
                await sync_to_async(text_model.save)()
                await sync_to_async(text_model.delete)()
        file.close()
    
        #audio = AudioFile.objects.filter(id=)
        return 

    def from_mp3_to_wav(self):
        sound = AudioSegment.from_mp3(self.file_path)
        sound.export(self.file_path, format="wav")
        return self.file_path
        
    def text_to_sentences(self):
        pass

