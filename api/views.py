from django.http import JsonResponse
from django.shortcuts import render
import json

# Create your views here.
def index(request):
  return render(request,'index.html')


from gtts import gTTS
import os

def text_to_speech(text, language='en', output_file='output.mp3'):
    tts = gTTS(text=text, lang=language,slow=True)
    tts.save(output_file)
  
def transcribe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        output_file = 'static/output.mp3'  # Ensure this file is served by Django
        text_to_speech(text, output_file=output_file)
        transcribed_text = "Successful!! Listen to it here..."
        audio_url = f'/{output_file}'  # Assuming the file is served from the static directory
        return JsonResponse({'transcribedText': transcribed_text, 'audioUrl': audio_url})
    return render(request, 'index.html')
