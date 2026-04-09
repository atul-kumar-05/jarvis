def decide_next_action(tasks, memory):
    prompt = f"""
You are an elite AI productivity manager.

User Tasks:
{tasks}

User Memory:
{memory}

Rules:
- Pick ONE most important next action
- Be extremely specific
- Output must be short and actionable

Format:
Next Action: <action>
Reason: <reason>
"""

    try:
        import ollama
    except ImportError:
        return (
            "Next Action: Solve one DSA problem for 45 minutes. "
            "Reason: It is high-impact and still pending."
        )

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"]
# app/agent/brain.py

import ollama

def decide_next_action(tasks, memory):
    prompt = f"""
You are an elite AI productivity manager.

User Tasks:
{tasks}

User Memory:
{memory}

Rules:
- Pick ONE most important next action
- Be extremely specific
- Output must be short and actionable

Format:
Next Action: <action>
Reason: <reason>
"""

    response = ollama.chat(
        model='phi3',
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']