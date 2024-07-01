import os
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.urls import reverse
from .forms import VoiceDataForm
from .models import VoiceData
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.applications import ResNet101
from datetime import datetime
import librosa
import matplotlib
matplotlib.use('Agg')  # 백엔드를 'Agg'로 설정하여 GUI 없이 작동하도록 설정
import matplotlib.pyplot as plt
from PIL import Image

def resnet_model():
    input_shape = (224, 224, 3)
    base_model = ResNet101(weights='imagenet', include_top=False, input_shape=input_shape)
    x = base_model.output
    x = Flatten()(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    return model

def upload_audio(request):
    if request.method == 'POST':
        form = VoiceDataForm(request.POST, request.FILES)
        if form.is_valid():
            voice_data = form.save(commit=False)
            voice_data.uploaded_at = datetime.now()
            voice_data.save()
            audio_path = voice_data.audio_file.path

            # 오디오 파일을 처리하고 MFCC를 추출
            audio_data, sample_rate = librosa.load(audio_path, sr=16000)
            mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)

            # MFCC를 이미지로 변환하고 저장
            plt.figure(figsize=(3.2, 3.2))  # 저장 시 224x224에 맞추기 위한 크기 설정
            librosa.display.specshow(mfccs, sr=sample_rate, x_axis='time')
            image_path = os.path.splitext(audio_path)[0] + '.png'
            plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
            plt.close()

            # 이미지를 로드하고 전처리
            image = Image.open(image_path).convert('RGB')
            image = image.resize((224, 224))
            image_array = np.array(image) / 255.0  # 정규화
            image_array = np.expand_dims(image_array, axis=0)  # 배치 차원 추가

            # 모델을 로드하고 예측 수행
            model = resnet_model()
            # 커스텀 학습 모델 파일이 있는 경우 아래 줄의 주석을 해제
            # model_path = os.path.join('voice_app', 'models', 'savemodel_101_all_Dense_32.h5')
            # model.load_weights(model_path)
            prediction = model.predict(image_array)

            # 예측 결과 저장
            voice_data.result = prediction[0][0]  # 이진 분류를 가정하고 필요에 따라 조정
            voice_data.save()
            
            return redirect(reverse('voice_app:result', args=[voice_data.id]))
    else:
        form = VoiceDataForm()
    return render(request, 'voice_app/upload.html', {'form': form})

def result(request, voice_id):
    audio = VoiceData.objects.get(id=voice_id)
    prediction = audio.result
    return render(request, 'voice_app/result.html', {'prediction': prediction})

##############################################################################################33
#  윈도우 버전

# import os
# import numpy as np
# import pandas as pd
# from django.shortcuts import render, redirect
# from django.core.files.storage import default_storage
# from django.urls import reverse
# from .forms import VoiceDataForm
# from .models import VoiceData
# from tensorflow.keras.models import load_model, Model
# from tensorflow.keras.layers import Dense, Flatten, Input
# from tensorflow.keras.applications import ResNet101
# from datetime import datetime
# import librosa
# import matplotlib
# matplotlib.use('Agg')  # 백엔드를 'Agg'로 설정하여 GUI 없이 작동하도록 설정
# import matplotlib.pyplot as plt
# from PIL import Image
# from pydub import AudioSegment

# # ffmpeg 경로 설정
# AudioSegment.converter = r"C:\Program Files (x86)\ffmpeg-2024-06-27-git-9a3bc59a38-full_build\bin\ffmpeg.exe"
# AudioSegment.ffprobe = r"C:\Program Files (x86)\ffmpeg-2024-06-27-git-9a3bc59a38-full_build\bin\ffprobe.exe"

# # 환경 변수 설정
# os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\ffmpeg-2024-06-27-git-9a3bc59a38-full_build\bin"


# def resnet_model():
#     input_shape = (224, 224, 3)
#     base_model = ResNet101(weights='imagenet', include_top=False, input_shape=input_shape)
#     x = base_model.output
#     x = Flatten()(x)
#     predictions = Dense(1, activation='sigmoid')(x)
#     model = Model(inputs=base_model.input, outputs=predictions)
    
#     return model

# def upload_audio(request):
#     if request.method == 'POST':
#         form = VoiceDataForm(request.POST, request.FILES)
#         if form.is_valid():
#             voice_data = form.save(commit=False)
#             voice_data.uploaded_at = datetime.now()
#             voice_data.save()
#             audio_path = voice_data.audio_file.path

#             # pydub을 사용하여 오디오 파일을 wav로 변환
#             audio = AudioSegment.from_file(audio_path)
#             wav_path = os.path.splitext(audio_path)[0] + '.wav'
#             audio.export(wav_path, format='wav')

#             # 오디오 파일을 처리하고 MFCC를 추출
#             audio_data, sample_rate = librosa.load(wav_path, sr=16000)
#             mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)

#             # MFCC를 이미지로 변환하고 저장
#             plt.figure(figsize=(3.2, 3.2))  # 저장 시 224x224에 맞추기 위한 크기 설정
#             librosa.display.specshow(mfccs, sr=sample_rate, x_axis='time')
#             image_path = os.path.splitext(audio_path)[0] + '.png'
#             plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
#             plt.close()

#             # 이미지를 로드하고 전처리
#             image = Image.open(image_path).convert('RGB')
#             image = image.resize((224, 224))
#             image_array = np.array(image) / 255.0  # 정규화
#             image_array = np.expand_dims(image_array, axis=0)  # 배치 차원 추가

#             # 모델을 로드하고 예측 수행
#             model = resnet_model()
#             # 커스텀 학습 모델 파일이 있는 경우 아래 줄의 주석을 해제
#             # model_path = os.path.join('voice_app', 'models', 'savemodel_101_all_Dense_32.h5')
#             # model.load_weights(model_path)
#             prediction = model.predict(image_array)

#             # 예측 결과 저장
#             voice_data.result = prediction[0][0]  # 이진 분류를 가정하고 필요에 따라 조정
#             voice_data.save()
            
#             return redirect(reverse('voice_app:result', args=[voice_data.id]))
#     else:
#         form = VoiceDataForm()
#     return render(request, 'voice_app/upload.html', {'form': form})

# def result(request, voice_id):
#     audio = VoiceData.objects.get(id=voice_id)
#     prediction = audio.result
#     return render(request, 'voice_app/result.html', {'prediction': prediction})
