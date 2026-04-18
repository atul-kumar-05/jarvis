# voice/assistant.py

from voice.input import listen
from voice.output import speak
from app.agent.manager import decide_next_action

def run_voice_assistant():

    text = listen()

    print("User said:", text)

    # simple intent routing (upgrade later)
    if "task" in text.lower():
        response = decide_next_action(text)
    else:
        response = "I will help you with that."

    print("AI:", response)

    speak(response)