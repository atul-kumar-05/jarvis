from datetime import datetime

behavior_log = []

def log_behavior(task,status):
    behavior_log.append({"task":task,"status":status,'time': datetime.now().hour})

def analyze_behavior(task,status):
    if not behavior_log:
        return 'No behavior log'

    skipped = sum(1 for x in behavior_log if x['status'] == 'skipped')
    completed = sum(1 for x in behavior_log if x['status'] == 'completed')

    if skipped > completed:
        return 'user is procrastinating'
    else:
        return 'user is consistent'

