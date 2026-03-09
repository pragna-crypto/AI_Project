from django import forms
from .models import SpeechAnalysis

class SpeechUploadForm(forms.ModelForm):
    class Meta:
        model = SpeechAnalysis
        fields = ['title', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter speech title'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
