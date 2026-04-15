from sqlalchemy.ext.asyncio import result

from app.llm import generate
from app.memory.behavior import log_behavior

def reviewer_node(state):
    result = state["result"]

    if not result:
        raise Exception("Executor is empty")
    prompt = f"""
    You are a performance reviewer.

    Executed Action:
    {result}

    Evaluate:
    - Is this effective?
    - Any improvement?

    Output:
    Feedback:
    Adjustment:
    """

    response = generate(prompt)

    log_behavior(state['task'],'completed')
    return {
        **state,
        'review_result': response
    }