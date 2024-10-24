from django.shortcuts import render
from .forms import UploadFileForm
import assemblyai as aai
from django.contrib import messages
import speech_recognition as sr
from pydub import AudioSegment

r = sr.Recognizer()


def transcribe_small_audio(path, language):
    with sr.AudioFile(path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language=language)
    return text



def index(request):
    context = None
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.success(request, ("Error!"))
            return render(request, 'recognition/index.html', {"error": "Provide a valid file"})
        
        try:
            file = request.FILES['audio_file']
            config = aai.TranscriptionConfig(language_code="ru")
            transcriber = aai.Transcriber(config=config)
            transcript = transcriber.transcribe(file.file)
            paragraphs = transcript.get_paragraphs()
            file.close()
            
            if transcript.error:
                context = {"error": transcript.error}
            else:
                context = {"transcript" : transcript.text,
                           "paragraphs" : paragraphs}
        except Exception as ex:
            context = {"error": str(ex)}
    return render(request, "recognition/index.html", context )