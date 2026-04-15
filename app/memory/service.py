from app.memory.vector_store import vector_store_index
from llama_index.core import Document

def store_memory(text : str):
    memory = Document(text=text)
    vector_store_index.insert(memory)

def retrieve_memory(query : str):
    query_engine = vector_store_index.as_query_engine(similarity_top_k=3)
    result = query_engine.query(query)
    return str(result)