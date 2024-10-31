from django import forms
from .models import AudioFile
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.ModelForm):
    audio = forms.FileField(
        widget=forms.FileInput(attrs={
            'type':'file',
            'class':'form-control'
        }
        ),
        help_text='Upload audio files',
        required=True,
        validators=[FileExtensionValidator(['mp3', 'ogg', 'wav'])]
    )
    class Meta:
        model = AudioFile
        fields = ['audio']
    
