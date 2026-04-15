from app.task.models import task

def score_of_task(task:task):
    score = 0

    if task.priority == 'high':
        score = 50
    elif task.score == 'medium':
        score = 30
    else:
        score = 10

    if task.status == 'pending':
        score += 20

    return score