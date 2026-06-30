import os
import pygame
import time

os.environ['SDL_AUDIODRIVER'] = 'alsa'
os.environ['AUDIODEV'] = 'hw:4,0'

#file_path = "/home/bready/Desktop/Work/output.wav"
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "output.wav")

pygame.mixer.init(
    #frequency=44100, size=-16, channels=2, buffer=512
    )

sound = pygame.mixer.Sound(file_path)
sound.play()

while pygame.mixer.get_busy():
    time.sleep(0.1)