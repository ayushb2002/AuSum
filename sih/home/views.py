from random import sample
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from google.cloud import speech

from dotenv import load_dotenv

from .forms import UploadForm

load_dotenv("../../")

def transcribe(request):
    if (request.method != "POST"):
        uploadForm = UploadForm()
        return render(request, "home/transcribe.html", {"form": uploadForm})
    else:
        client = speech.SpeechClient()
        form = UploadForm(request.POST, request.FILES)
        if (not form.is_valid()):
            return render(request, "home/error.html", {"form": form})
        file = form.files['file']
        if (file):
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            audioFile = None
            with fs.open("D:\\FullStackDevelopment\\sih_aiml\\sih"+file_url, 'rb') as audioFileObj:
                audioFile = audioFileObj.read()
            audio = speech.RecognitionAudio(content=audioFile)
            config = speech.RecognitionConfig(
                enable_automatic_punctuation=True,
                sample_rate_hertz=48000,
                language_code="en-US"
            )

            response = client.recognize(config=config, audio=audio)
            spresults = ""
            for result in response.results:
                spresults+=result.alternatives[0].transcript
        return render(request, "home/transcribe.html", {"result": spresults})

def index(request):
    return render(request, "home/index.html")
