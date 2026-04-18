# voice/input.py

from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np

model = WhisperModel("base")

def listen():

    print("🎤 Listening...")

    audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1)
    sd.wait()

    segments, _ = model.transcribe(audio.flatten())

    text = " ".join([seg.text for seg in segments])

    return text