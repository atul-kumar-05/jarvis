from app.llm import generate

def executer_node(state):
    plan = state["plan"]
    print(plan)
    if not plan:
        raise Exception("Plan is empty")

    prompt = f"""You are an execution agent.
                Plan:{plan}
                Pick the FIRST step and convert it into:
                - A concrete action
                - With time estimate
                
                Output:
                Action:
                Time:
                """

    result = generate(prompt)
    return {
       **state,
       'result': result
    }