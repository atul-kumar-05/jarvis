from app.memory.service import store_memory
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

    review = generate(prompt)

    success = 'good' in review.lower()

    store_memory(state['task'], result, review, success)


    log_behavior(state['task'],'completed')
    return {
        **state,
        'review_result': review
    }