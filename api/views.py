from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
import json
from google.oauth2 import service_account

# Create your views here.
def index(request):
  return render(request,'index.html')


import os
from gtts import gTTS
from google.cloud import storage

# Function to convert text to speech and save to a file
def text_to_speech(text, output_file):
    tts = gTTS(text)
    tts.save(output_file)

# Function to handle the transcribe request
def transcribe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')

        # Use /tmp directory for temporary storage
        output_dir = '/tmp'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = os.path.join(output_dir, 'output.mp3')
        text_to_speech(text, output_file=output_file)
        
        print("Before Credentials")
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        # Upload the file to Google Cloud Storage
        GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        credentials_info = json.loads(GOOGLE_APPLICATION_CREDENTIALS)
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        storage_client = storage.Client(credentials=credentials)
        # storage_client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
        bucket_name = 'text-transcription-1' 
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('output.mp3')
        blob.upload_from_filename(output_file)
        
        # Generate the file URL
        audio_url = blob.generate_signed_url(
            version='v4',
            expiration=timedelta(minutes=15),  # URL will be valid for 15 minutes
            method='GET'
        )
        print(blob.public_url)
        transcribed_text = "Successful!! Listen to it here..."
        return JsonResponse({'transcribedText': transcribed_text, 'audioUrl': audio_url})
    
    return render(request, 'index.html')

