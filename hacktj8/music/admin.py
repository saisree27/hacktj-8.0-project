from django.contrib import admin
from .models import File
from .forms import UploadFileForm

# Register your models here.

class FileAdmin(admin.TabularInline):
    model = File
    list_display = ['filename', 'document']

admin.site.register(File)