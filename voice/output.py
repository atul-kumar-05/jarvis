# voice/output.py

"""Text-to-speech output using gTTS and pygame."""

import os
import tempfile
import time

from gtts import gTTS
import pygame


def speak(text: str) -> None:
    """
    Convert text to speech and play through the default audio device.

    Uses a temporary file instead of a hardcoded filename to avoid
    race conditions when called concurrently.
    """
    tmp_file = None
    try:
        # Create a temporary MP3 file
        tmp_file = tempfile.NamedTemporaryFile(
            suffix=".mp3", delete=False
        )
        tmp_path = tmp_file.name
        tmp_file.close()

        tts = gTTS(text)
        tts.save(tmp_path)

        pygame.mixer.init()
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()
    except Exception as exc:
        print(f"⚠️  Speech output failed: {exc}")
    finally:
        if tmp_file and os.path.exists(tmp_path):
            os.remove(tmp_path)