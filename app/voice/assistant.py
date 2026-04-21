# app/voice/assistant.py

"""Jarvis Voice Assistant -- continuous interaction loop."""

import sys
import io
from datetime import datetime

# Force UTF-8 output on Windows so emoji don't crash
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.core.logging import logger
from app.config.database import SessionLocal
from app.services.task_service import get_pending_tasks, get_top_task_with_score
from app.voice.speech_output import speak
from app.voice.command_processor import process_command
from app.voice.intent_parser import parse_voice_command


def _build_greeting(db) -> str:
    hour = datetime.now().hour
    pending = get_pending_tasks(db)
    count = len(pending)
    time_greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")
    greeting = f"{time_greeting}, sir. I'm Jarvis, your task assistant."
    if count == 0:
        greeting += " You have no pending tasks."
    elif count == 1:
        greeting += f" You have 1 pending task: '{pending[0].title}'."
    else:
        top_task, score, reason = get_top_task_with_score(db)
        greeting += f" You have {count} pending tasks. I recommend starting with '{top_task.title}' because {reason}."
    return greeting


def run_voice_assistant(text_mode: bool = False) -> None:
    """Run the Jarvis voice assistant in a continuous loop."""
    db = SessionLocal()
    try:
        greeting = _build_greeting(db)
        _print(f"\n[JARVIS] {greeting}\n")
        speak(greeting)
        print("=" * 60)
        print("[TEXT MODE]" if text_mode else "[VOICE MODE] Listening via microphone")
        print("Say 'help' to see available commands")
        print("=" * 60)

        from app.voice.speech_input import listen

        while True:
            try:
                if text_mode:
                    user_input = input("\n[You]: ").strip()
                else:
                    user_input = listen(duration_seconds=5)
                if not user_input:
                    continue
                if user_input.lower() in ("quit", "exit", "stop", "bye"):
                    farewell = "Goodbye, sir. I'll be here when you need me."
                    _print(f"\n[JARVIS] {farewell}")
                    speak(farewell)
                    break
                _print(f"[You]: {user_input}")
                cmd = parse_voice_command(user_input)
                response = process_command(cmd, db)
                _print(f"[JARVIS] {response.spoken_response}")
                speak(response.spoken_response)
            except KeyboardInterrupt:
                _print("\n[JARVIS] Goodbye, sir.")
                break
            except Exception as exc:
                logger.error("Voice loop error: %s", exc)
                _print("[JARVIS] I encountered an error. Let me try again.")
    finally:
        db.close()


def _print(msg: str) -> None:
    """Print safely on Windows terminals that don't support UTF-8 emoji."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='replace').decode('ascii'))


if __name__ == "__main__":
    run_voice_assistant(text_mode="--text" in sys.argv)
