from app.memory.service import retrieve_memory, rank_memory

def build_context(task, behavior):
    context = retrieve_memory(task)
    rank_mem = rank_memory(context)

    return f'''past experience:{rank_mem},
               behavior:{behavior}'''
