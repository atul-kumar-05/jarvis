

def create_tasks_from_plan(plan_text):

    lines = plan_text.split("\n")

    for line in lines:
        if line.strip():
            create_task(
                title=line.strip(),
                priority="medium"
            )