from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from .forms import UploadFileForm
from .models import File
import random
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU') 
# tf.config.experimental.set_memory_growth(physical_devices[0], True)
from sklearn.preprocessing import StandardScaler
import librosa
import numpy as np
import pickle
import os
import base64

# Create your views here.


def index(request):
    return render(request, 'music/index.html')


def genre(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if 'document' in request.FILES and form.is_valid():
            file_sent = request.FILES['document']
            newfile = File(filename=file_sent.name + "_" + str(random.getrandbits(64)), document=file_sent)
            newfile.save() # save to sqlite

            answer = process_file_upload(file_sent)
            # form.save()
            return render(request, 'music/genre.html', {'message': answer, 'form': form})
        else:
            return render(request, 'music/genre.html', {'message': 'Attach a file before submitting!', 'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'music/genre.html', {'message': '', 'form': form})

def generation(request):
    if request.method == 'POST':
        print(request.POST)
        genre = request.POST.get('genre')
        print(genre)
        # audiofile = generate_music(file_sent) # assuming file is correct type
        pwd = os.path.dirname(__file__)
        audiofile = pwd + '/static/audio/hiphop.wav'
        
        enc = base64.b64encode(open(audiofile, "rb").read())
        fr = JsonResponse({'file': enc.decode('utf-8'), "filetype": audiofile.split(".")[-1]})
        return fr
    return render(request, 'music/generation.html', {'message': ''})











def process_file_upload(file_sent):
    extension = file_sent.name.split(".")[-1]
    print(extension)
    if extension not in ["wav", "mp3", "ogg"]:
        print("Not correct filetype.")
        return
    with open("temp." + extension, 'wb+') as destination:
        for chunk in file_sent.chunks():
            destination.write(chunk)
    
    pwd = os.path.dirname(__file__)
    print(pwd)
    features = extract_features("temp." + extension)
    feature_array = [[features[x] for x in features.keys()]]
    scaler = pickle.load(open(pwd + '/static/assets/scaler.pkl', 'rb'))
    X = np.array(feature_array, dtype=float)
    X_transformed = scaler.transform(X.reshape(1,-1))
    model = tf.keras.models.load_model(pwd + '/static/assets/best_model_75.h5')
    y_pred = model.predict(X_transformed)
    categories = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    print(categories[np.argmax(y_pred)])
    return categories[np.argmax(y_pred)]

def extract_features(songname):
    features = {
        'length': '', 'chroma_stft_mean': '', 'chroma_stft_var': '', 'rms_mean': '', 'rms_var': '',
       'spectral_centroid_mean': '', 'spectral_centroid_var': '',
       'spectral_bandwidth_mean': '', 'spectral_bandwidth_var': '', 'rolloff_mean': '',
       'rolloff_var': '', 'zero_crossing_rate_mean': '', 'zero_crossing_rate_var': '',
       'harmony_mean': '', 'harmony_var': '', 'perceptr_mean': '', 'perceptr_var': '', 'tempo': '',
       'mfcc1_mean': '', 'mfcc1_var': '', 'mfcc2_mean': '', 'mfcc2_var': '', 'mfcc3_mean': '',
       'mfcc3_var': '', 'mfcc4_mean': '', 'mfcc4_var': '', 'mfcc5_mean': '', 'mfcc5_var': '',
       'mfcc6_mean': '', 'mfcc6_var': '', 'mfcc7_mean': '', 'mfcc7_var': '', 'mfcc8_mean': '',
       'mfcc8_var': '', 'mfcc9_mean': '', 'mfcc9_var': '', 'mfcc10_mean': '', 'mfcc10_var': '',
       'mfcc11_mean': '', 'mfcc11_var': '', 'mfcc12_mean': '', 'mfcc12_var': '', 'mfcc13_mean': '',
       'mfcc13_var': '', 'mfcc14_mean': '', 'mfcc14_var': '', 'mfcc15_mean': '', 'mfcc15_var': '',
       'mfcc16_mean': '', 'mfcc16_var': '', 'mfcc17_mean': '', 'mfcc17_var': '', 'mfcc18_mean': '',
       'mfcc18_var': '', 'mfcc19_mean': '', 'mfcc19_var': '', 'mfcc20_mean': '', 'mfcc20_var': ''
    }
    y, sr = librosa.load(songname, mono=True, duration=30)
    length = 661794
    chroma_stft_mean, chroma_stft_var = np.mean(librosa.feature.chroma_stft(y=y, sr=sr)), np.var(librosa.feature.chroma_stft(y=y, sr=sr))
    rms_mean, rms_var = np.mean(librosa.feature.rms(y=y)), np.var(librosa.feature.rms(y=y))
    spectral_centroid_mean, spectral_centroid_var = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)), np.var(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth_mean, spectral_bandwidth_var = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)), np.var(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    rolloff_mean, rolloff_var = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)), np.var(librosa.feature.spectral_rolloff(y=y, sr=sr))
    zcr_mean, zcr_var = np.mean(librosa.feature.zero_crossing_rate(y)), np.var(librosa.feature.zero_crossing_rate(y))
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    y_harm, y_perc = librosa.effects.hpss(y)
    harmony_mean, harmony_var = np.mean(y_harm), np.var(y_harm)
    perceptr_mean, perceptr_var = np.mean(y_perc), np.var(y_perc)
    
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    list_mfccs = [ (0,0) for x in range(0, 21) ]
    for index, x in enumerate(mfcc):
        list_mfccs[index] = (np.mean(x), np.var(x))
    
    
    features['length'] = length
    features['chroma_stft_mean'] = chroma_stft_mean
    features['chroma_stft_var'] = chroma_stft_var
    features['rms_mean'] = rms_mean
    features['rms_var'] = rms_var
    features['spectral_centroid_mean'] = spectral_centroid_mean
    features['spectral_centroid_var'] = spectral_centroid_var
    features['spectral_bandwidth_mean'] = spectral_bandwidth_mean
    features['spectral_bandwidth_var'] = spectral_bandwidth_var
    features['rolloff_mean'] = rolloff_mean
    features['rolloff_var'] = rolloff_var
    features['zero_crossing_rate_mean'] = zcr_mean
    features['zero_crossing_rate_var'] = zcr_var
    features['harmony_mean'] = harmony_mean
    features['harmony_var'] = harmony_var
    features['perceptr_mean'] = perceptr_mean
    features['perceptr_var'] = perceptr_var
    features['tempo'] = tempo
    features['mfcc1_mean']  = list_mfccs[0][0]
    features['mfcc1_var']   = list_mfccs[0][1]
    features['mfcc2_mean']  = list_mfccs[1][0]
    features['mfcc2_var']   = list_mfccs[1][1]
    features['mfcc3_mean']  = list_mfccs[2][0]
    features['mfcc3_var']   = list_mfccs[2][1]
    features['mfcc4_mean']  = list_mfccs[3][0]
    features['mfcc4_var']   = list_mfccs[3][1]
    features['mfcc5_mean']  = list_mfccs[4][0]
    features['mfcc5_var']   = list_mfccs[4][1]
    features['mfcc6_mean']  = list_mfccs[5][0]
    features['mfcc6_var']   = list_mfccs[5][1]
    features['mfcc7_mean']  = list_mfccs[6][0]
    features['mfcc7_var']   = list_mfccs[6][1]
    features['mfcc8_mean']  = list_mfccs[7][0]
    features['mfcc8_var']   = list_mfccs[7][1]
    features['mfcc9_mean']  = list_mfccs[8][0]
    features['mfcc9_var']   = list_mfccs[8][1]
    features['mfcc10_mean'] = list_mfccs[9][0]
    features['mfcc10_var']  = list_mfccs[9][1]
    features['mfcc11_mean'] = list_mfccs[10][0]
    features['mfcc11_var']  = list_mfccs[10][1]
    features['mfcc12_mean'] = list_mfccs[11][0]
    features['mfcc12_var']  = list_mfccs[11][1]
    features['mfcc13_mean'] = list_mfccs[12][0]
    features['mfcc13_var']  = list_mfccs[12][1]
    features['mfcc14_mean'] = list_mfccs[13][0]
    features['mfcc14_var']  = list_mfccs[13][1]
    features['mfcc15_mean'] = list_mfccs[14][0]
    features['mfcc15_var']  = list_mfccs[14][1]
    features['mfcc16_mean'] = list_mfccs[15][0]
    features['mfcc16_var']  = list_mfccs[15][1]
    features['mfcc17_mean'] = list_mfccs[16][0]
    features['mfcc17_var']  = list_mfccs[16][1]
    features['mfcc18_mean'] = list_mfccs[17][0]
    features['mfcc18_var']  = list_mfccs[17][1]
    features['mfcc19_mean'] = list_mfccs[18][0]
    features['mfcc19_var']  = list_mfccs[18][1]
    features['mfcc20_mean'] = list_mfccs[19][0]
    features['mfcc20_var']  = list_mfccs[19][1]
    
    return features    


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
