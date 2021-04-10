from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'music/index.html')

def genre(request):
    return render(request, 'music/genre.html')

def generation(request):
    return render(request, 'music/generation.html')