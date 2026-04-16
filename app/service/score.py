from app.task.models import task

from datetime import datetime

def score_task(task, behavior):

    score = 0

    # Priority
    if task.priority == "high":
        score += 50
    elif task.priority == "medium":
        score += 30
    else:
        score += 10

    # Behavior adjustment
    if "procrastinating" in behavior.lower():
        score -= 10  # avoid heavy tasks

    # Time-based optimization
    current_hour = datetime.now().hour

    if 6 <= current_hour <= 12:
        score += 20  # deep work window
    elif 18 <= current_hour <= 23:
        score -= 10  # low energy

    return score