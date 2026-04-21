# app/voice/speech_input.py

"""Voice input — captures audio from microphone and transcribes via Google Speech Recognition.

Uses the SpeechRecognition library with Google's free cloud API.
No model download required — works out of the box.
"""

from app.core.logging import logger


def listen(duration_seconds: int = 5, sample_rate: int = 16000) -> str:
    """Record audio from the microphone and transcribe it using Google Speech Recognition."""
    try:
        import speech_recognition as sr
    except ImportError:
        logger.error("SpeechRecognition not installed. Run: pip install SpeechRecognition pyaudio")
        return ""

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone(sample_rate=sample_rate) as source:
            # Quickly calibrate for background noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print(f"🎤 Listening... (speak now, up to {duration_seconds}s)")
            audio = recognizer.listen(source, timeout=duration_seconds, phrase_time_limit=duration_seconds)

        print("⏳ Transcribing...")
        text = recognizer.recognize_google(audio)
        logger.info("Transcribed: '%s'", text[:100])
        print(f"✅ Heard: '{text}'")
        return text

    except sr.WaitTimeoutError:
        print("🔇 No speech detected (timeout)")
        return ""
    except sr.UnknownValueError:
        print("🤔 Could not understand audio")
        return ""
    except sr.RequestError as exc:
        logger.error("Google Speech Recognition request failed: %s", exc)
        print("🔌 Speech recognition failed — check your internet connection")
        return ""
    except OSError as exc:
        logger.error("Microphone error: %s", exc)
        print(f"🎙️ Microphone not available: {exc}")
        return ""
    except Exception as exc:
        logger.error("Voice input failed: %s", exc)
        return ""
