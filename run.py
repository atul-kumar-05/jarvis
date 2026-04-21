"""
Jarvis Voice Assistant launcher.

Usage:
    python run.py              → Voice mode (uses microphone)
    python run.py --text       → Text mode (type commands)
"""

import sys
from app.voice.assistant import run_voice_assistant

if __name__ == "__main__":
    text_mode = "--text" in sys.argv
    run_voice_assistant(text_mode=text_mode)
