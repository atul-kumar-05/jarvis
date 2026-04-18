# voice/assistant.py

"""Voice assistant — listens, detects intent, and acts."""

from voice.input import listen
from voice.output import speak
from voice.router import detect_intent

from app.agent.manager import decide_next_action
from app.db.db import SessionLocal
from app.task.service import create_task


def run_voice_assistant() -> None:
    """Run a single voice interaction cycle: listen → intent → act → speak."""

    text = listen()
    print("User:", text)

    intent = detect_intent(text)

    if intent == "add_task":
        task_title = text.lower().replace("add task", "").strip()
        if task_title:
            create_task(title=task_title, priority="medium")
            response = f"Task added: {task_title}"
        else:
            response = "Please specify a task title after 'add task'."

    elif intent == "next_action":
        db = SessionLocal()
        try:
            result = decide_next_action(db)
            response = result.get("message", str(result))
        finally:
            db.close()

    elif intent == "get_task":
        response = "You can view your tasks at http://localhost:8000/tasks"

    else:
        response = "I can help you manage tasks and plan your day. Try 'add task' or 'what should I do next'."

    print("AI:", response)
    speak(response)