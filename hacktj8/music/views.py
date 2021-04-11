from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from .models import File
import random

# Create your views here.


def index(request):
    return render(request, 'music/index.html')


def genre(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if 'document' in request.FILES and form.is_valid():
            file = request.FILES['document']
            newfile = File(filename=file.name + "_" + str(random.getrandbits(64)), document=file)
            newfile.save() # save to sqlite

            process_file_upload(file)
            # form.save()
            return render(request, 'music/genre.html', {'message': 'File sent!', 'form': form})
        else:
            return render(request, 'music/genre.html', {'message': 'Attach a file before submitting!', 'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'music/genre.html', {'message': '', 'form': form})

def generation(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        print(genre)
        audiofile = generate_music(genre)
        return HttpResponse(audiofile)
    return render(request, 'music/generation.html')

def process_file_upload(file):
    print(file.read())

def generate_music(genre):
    # switch cases
    audiofile = "woooooooooooooooo"
    return audiofile


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('upload_file')
#     else:
#         form = UploadFileForm()
#     return render(request, 'music/genre.html', {'form': form})
