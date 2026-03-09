import os
import wave
import contextlib
import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SpeechAnalysis
from .forms import SpeechUploadForm

# Analysis libraries
import speech_recognition as sr
import librosa
import numpy as np

@login_required
def index(request):
    return render(request, 'analyzer/index.html')

@login_required
def upload_speech(request):
    if request.method == 'POST':
        form = SpeechUploadForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save()
            # Perform Analysis
            process_audio(analysis)
            return redirect('results', pk=analysis.pk)
    else:
        form = SpeechUploadForm()
    
    return render(request, 'analyzer/upload.html', {'form': form})

def process_audio(analysis):
    audio_path = analysis.audio_file.path
    
    # Simple speech analysis using speech_recognition and librosa
    recognizer = sr.Recognizer()
    transcript = "Transcript could not be generated."
    word_count = 0
    
    try:
        # Note: Depending on OS, librosa loading might need audio format conversions. 
        # But for simplification we'll assume audio is readable by librosa and SR if it's WAV.
        # Alternatively, librosa can read mp3/wav and calculate duration.
        y, sr_rate = librosa.load(audio_path, sr=16000)
        duration_sec = librosa.get_duration(y=y, sr=sr_rate)
        
        # Just writing a temporary wav for speech recognition
        import soundfile as sf
        temp_wav = audio_path + "_temp.wav"
        sf.write(temp_wav, y, sr_rate)
        
        with sr.AudioFile(temp_wav) as source:
            audio_data = recognizer.record(source)
            try:
                transcript = recognizer.recognize_google(audio_data)
                words = transcript.lower().split()
                word_count = len(words)
            except Exception as e:
                transcript = f"Recognition error: {e}"
        
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
            
        # Analysis calculations
        duration_min = duration_sec / 60.0 if duration_sec > 0 else 1
        speech_speed_wpm = word_count / duration_min
        
        # Filler words
        filler_words = ['um', 'uh', 'like', 'you know', 'so', 'actually']
        filler_words_count = sum(1 for w in words if w in filler_words) if word_count > 0 else 0
        
        # Pauses using librosa
        non_mute_intervals = librosa.effects.split(y, top_db=20)
        pause_count = len(non_mute_intervals) - 1 if len(non_mute_intervals) > 0 else 0
        
        # Volume stability using RMS
        rms = librosa.feature.rms(y=y)
        voice_volume_stability = float(np.std(rms) * 100) # Standard dev of RMS * 100
        
        # Simple scoring logic
        
        # Rate: ideal 130-160 wpm
        if 130 <= speech_speed_wpm <= 160:
            speed_score = 25.0
        else:
            speed_score = max(0.0, 25.0 - abs(speech_speed_wpm - 145) * 0.2)
            
        # Filler words
        filler_score = max(0.0, 25.0 - filler_words_count * 2.0)
        
        # Pauses
        pause_score = max(0.0, 25.0 - pause_count * 1.5)
        
        # Stability (lower std dev is more stable)
        stability_score = max(0.0, 25.0 - voice_volume_stability * 2.0)
        
        # Overall confidence score
        confidence_score = speed_score + filler_score + pause_score + stability_score
        
        suggestions = []
        if speech_speed_wpm < 120:
            suggestions.append("Try speaking a bit faster to keep the audience engaged.")
        elif speech_speed_wpm > 170:
            suggestions.append("You are speaking too fast. Take breaths and slow down.")
        
        if filler_words_count > 5:
            suggestions.append("You use too many filler words (um, uh). Practice pausing instead.")
            
        if pause_count > 10:
            suggestions.append("There are many awkward pauses. Try practicing the speech more smoothly.")
            
        suggestions_text = " \\n".join(suggestions) if suggestions else "Great speaking skills! Keep it up."
        
        # Update model
        analysis.speech_speed_wpm = round(speech_speed_wpm, 2)
        analysis.filler_words_count = filler_words_count
        analysis.pause_count = pause_count
        analysis.voice_volume_stability = round(voice_volume_stability, 3)
        analysis.speed_score = round(speed_score, 2)
        analysis.filler_score = round(filler_score, 2)
        analysis.pause_score = round(pause_score, 2)
        analysis.stability_score = round(stability_score, 2)
        analysis.confidence_score = round(confidence_score, 2)
        analysis.transcript = transcript
        analysis.suggestions = suggestions_text
        analysis.save()
        
    except Exception as e:
        print(f"Error processing audio: {e}")
        analysis.transcript = "Error processing audio. Did you provide a valid standard Audio file?"
        analysis.save()

@login_required
def results(request, pk):
    analysis = get_object_or_404(SpeechAnalysis, pk=pk)
    
    # Chart data
    labels = ['Speech Speed', 'Filler Words', 'Pauses', 'Voice Stability']
    scores = [
        analysis.speed_score or 0,
        analysis.filler_score or 0,
        analysis.pause_score or 0,
        analysis.stability_score or 0
    ]
    
    context = {
        'analysis': analysis,
        'chart_labels': labels,
        'chart_scores': scores
    }
    return render(request, 'analyzer/results.html', context)

@login_required
def history(request):
    analyses = SpeechAnalysis.objects.all().order_by('-created_at')
    
    # Progress Data
    progress_dates = []
    progress_scores = []
    for a in analyses.order_by('created_at'):
        progress_dates.append(a.created_at.strftime('%Y-%m-%d %H:%M'))
        progress_scores.append(a.confidence_score or 0)
        
    context = {
        'analyses': analyses,
        'progress_dates': progress_dates,
        'progress_scores': progress_scores
    }
    return render(request, 'analyzer/history.html', context)
