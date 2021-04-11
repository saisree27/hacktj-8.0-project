from django import forms
from .models import File

class UploadFileForm(forms.ModelForm):

    # def is_valid(file):
    #     if file != None:


    class Meta:
        model = File
        fields = ('document', )
