# voice/output.py

from gtts import gTTS
import pygame
import os
import time


def speak(text):
    filename = "output.mp3"

    tts = gTTS(text)
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()
    os.remove(filename)


em("start output.mp3")  # Windows