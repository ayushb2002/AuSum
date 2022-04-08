from random import sample
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from google.cloud import speech

from dotenv import load_dotenv

load_dotenv("../../")

def transcribe(request):
    if (request.method != "POST"):
        return render(request, "home/transcribe.html")
    else:
        client = speech.SpeechClient()
        file = request.FILES['file']
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
        return render(request, "home/success.html", {"result": spresults})

def index(request):
    return render(request, "home/index.html")
