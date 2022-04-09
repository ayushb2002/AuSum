from random import sample
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from google.cloud import speech

from dotenv import load_dotenv

from .forms import UploadForm

import os
import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import nltk
import re
from nltk.corpus import stopwords

load_dotenv("../../")

def generateSummary(para, n=5):
  sent_list = nltk.sent_tokenize(para)
  if n>len(sent_list)/2:
    return "Summary cannot be greater in length than half of provided data!"
  post_punctuation = [] 
  punctuation = re.compile(r'[-.?!,:;()|0-9]')
  for sentences in sent_list:
    sent = punctuation.sub(" ", sentences)
    sent = re.sub(r'\[[0-9]*\]', ' ', sentences)
    sent = re.sub(r'\s+', ' ', sentences)
    if len(sent)>0:
      post_punctuation.append(sent)
  
  formatted_str = ' '.join([str(pp) for pp in post_punctuation])
  stopwords = nltk.corpus.stopwords.words('english')

  word_frequencies = {}
  for word in nltk.word_tokenize(formatted_str):
      if word not in stopwords:
          if word not in word_frequencies.keys():
              word_frequencies[word] = 1
          else:
              word_frequencies[word] += 1

  maximum_frequncy = max(word_frequencies.values())

  for word in word_frequencies.keys():
      word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)  

  sentence_scores = {}
  for sent in sent_list:
      for word in nltk.word_tokenize(sent.lower()):
          if word in word_frequencies.keys():
              if len(sent.split(' ')) < 30:
                  if sent not in sentence_scores.keys():
                      sentence_scores[sent] = word_frequencies[word]
                  else:
                      sentence_scores[sent] += word_frequencies[word]  

  summary_sentences = heapq.nlargest(n, sentence_scores, key=sentence_scores.get)

  summary = ' '.join(summary_sentences)
  return summary

def generateNotes(para, n=3):
  sent_list = nltk.sent_tokenize(para)

  if n>len(sent_list)/2:
      return "Summary cannot be greater in length than half of provided data!"

  post_punctuation = [] 
  punctuation = re.compile(r'[-.?!,:;()|0-9]')
  for sentences in sent_list:
    sent = punctuation.sub(" ", sentences)
    sent = re.sub(r'\[[0-9]*\]', ' ', sentences) #removes square brackets
    sent = re.sub(r'\s+', ' ', sentences) #removes extra spaces
    sent = re.sub(r"\([^()]*\)", '', sentences) #removes parenthesis
    if len(sent)>0:
      post_punctuation.append(sent)

  formatted_str = ' '.join([str(pp) for pp in post_punctuation])
  stopwords = nltk.corpus.stopwords.words('english')

  word_frequencies = {}
  for word in nltk.word_tokenize(formatted_str):
      if word not in stopwords:
          if word not in word_frequencies.keys():
              word_frequencies[word] = 1
          else:
              word_frequencies[word] += 1

  maximum_frequncy = max(word_frequencies.values())

  for word in word_frequencies.keys():
      word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)  

  sentence_scores = {}
  for sent in sent_list:
      for word in nltk.word_tokenize(sent.lower()):
          if word in word_frequencies.keys():
              if len(sent.split(' ')) < 30:
                  if sent not in sentence_scores.keys():
                      sentence_scores[sent] = word_frequencies[word]
                  else:
                      sentence_scores[sent] += word_frequencies[word]  

  notes = []
  for sent in post_punctuation:
    newSent = ""
    if sent not in stopwords:
        newSent+=sent+" "
    notes.append(newSent)

    note = {}

  i=0
  for key in sentence_scores:
    note[notes[i]] = sentence_scores[key]
    i+=1

  notes_sentences = heapq.nlargest(n, note, key=note.get)
  
  # punctuated_notes = []
  # for i in range(len(notes_sentences)):
  #   punctuated_notes.append(punctuate(notes_sentences[i]))

  return notes_sentences

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
        return render(request, "home/notes.html", {"data": True, "result": spresults, "summary": False})

def index(request):
    return render(request, "home/index.html")

def summarize(request):
    return render(request, "home/summarize.html", {"data": False, "summary": False})

def loadSummary(request):
    if request.method == "GET":
        txtFS = request.GET['txtarea']
        context = {
            "content": generateSummary(txtFS),
            "data": True,
            "result": txtFS, 
            "summary": True
        }
        return render(request, "home/summarize.html", context)
    else:
        return HttpResponse('Wrong request!')

def notes(request):
    return render(request, "home/notes.html", {"data": False, "notes": False})

def loadNotes(request):
    if request.method == "GET":
        txtFS = request.GET['txtarea']
        context = {
            "content": generateNotes(txtFS),
            "data": True,
            "result": txtFS, 
            "notes": True
        }
        return render(request, "home/notes.html", context)
    else:
        return HttpResponse('Wrong request!')