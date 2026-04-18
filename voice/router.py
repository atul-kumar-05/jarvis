"""Voice intent router — maps spoken text to action intents."""


def detect_intent(voice: str) -> str:
    """
    Detect the user's intent from voice input text.

    Args:
        voice: Transcribed voice text.

    Returns:
        Intent string: ``"add_task"``, ``"remove_task"``,
        ``"next_action"``, or ``"unknown"``.
    """
    lower = voice.lower()

    if "add task" in lower:
        return "add_task"
    elif "remove task" in lower:
        return "remove_task"
    elif "next" in lower or "what should i do" in lower:
        return "next_action"
    elif "get task" in lower or "list task" in lower:
        return "get_task"
    else:
        return "unknown"