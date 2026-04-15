from app.memory.rag_service import retrieve_context
from app.llm import generate
from app.memory.behavior import analyze_behavior


def planner_node(state):
    task = state["task"]
    context = retrieve_context()
    behavior = analyze_behavior(task,task.status)
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

