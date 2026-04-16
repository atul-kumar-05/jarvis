from datetime import datetime

from app.memory.vector_store import vector_store_index
from llama_index.core import Document
from datetime import datetime

def store_memory(text, result, review, success : bool):
    text = Document(text= f'''
        Task: {text}
        Review: {review}
        result: {result}
        Success: {success}
        ''',
        metadata = {
        'review': review,
        'success': success,
        'text': text,
        'timestamp': datetime.datetime.now().isoformat(),
        'type':'execution'
    })
    vector_store_index.insert(text)

def retrieve_memory(query : str):
    query_engine = vector_store_index.as_query_engine(similarity_top_k=3)
    result = query_engine.query(query)
    return str(result)

def rank_memory(memory : str):
    if 'failed' in memory.lower():
        return 'failed'
    return memory