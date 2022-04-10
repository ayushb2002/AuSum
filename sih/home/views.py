from multiprocessing import context
from random import sample
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from google.cloud import speech
from dotenv import load_dotenv
from .forms import UploadForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

load_dotenv("../../")

def registerPage(request):
    form = CreateUserForm()

    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+user)
            return redirect('login')

    context={'form':form}
    return render(request,"home/register.html", context)

def loginPage(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')


    context={}
    return render(request,"home/login.html", context)

def logoutUser(request):
    logout(request)
    return redirect('login')

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
