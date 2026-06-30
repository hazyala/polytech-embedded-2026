import os

import sounddevice as sd
import scipy.io as sio
import scipy.io.wavfile
# numpy array audio data, frames per second
sample_rate = 44100  # 샘플레이트, 
seconds = 3  # 녹음시간

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "output.wav")

print("녹음 시작..녹음중")
myrecording = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()  # 녹음이 끝날때까지 대기
print("녹음 완료")
sio.wavfile.write(file_path, sample_rate, myrecording)  # wav파일로 저장