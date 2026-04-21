"""Executor agent prompt templates."""

EXECUTOR_PROMPT = """
You are an execution agent.

Plan:
{plan}

Pick the FIRST step and convert it into:
- A concrete action
- With time estimate

Output:
Action:
Time:
"""
