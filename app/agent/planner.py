from app.memory.rag_service import build_context
from app.llm import generate
from app.memory.behavior import analyze_behavior


def planner_node(state):
    task = state["task"]
    behavior = analyze_behavior(task,task.status)
    context = build_context(task,behavior)
    prompt = f"""
You are an elite planning agent.

Task:
{task}

Context:
{context}

Behaviour: {behavior}

Break this into 3-5 clear, actionable steps.

Rules:
- Keep steps small
- Execution-ready
- No fluff

Output:
Step 1:
Step 2:
...
"""
    plan = generate(prompt)
    print (plan)

    return {
        **state,
        "plan": plan
    }

def generate_tasks_from_goal(goal):

    prompt = f"""
You are an elite planning agent.

Goal:
{goal}

Break this into 5 actionable tasks.

Rules:
- Tasks must be executable
- Keep them small
- Focus on progress

Output:
1.
2.
3.
"""

    return generate(prompt)

