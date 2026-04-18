from datetime import datetime
from app.memory.vector_store import get_index
from llama_index.core import Document

def store_memory(task_obj, result, review, success : bool):
    
    if not isinstance(task_obj, str):
        if hasattr(task_obj, 'title') and hasattr(task_obj, 'description'):
            task_str = f"{task_obj.title} {task_obj.description}"
        else:
            task_str = str(task_obj)
    else:
        task_str = task_obj

    # Create document with serializable metadata
    doc = Document(
        text=f'''
        Task: {task_str}
        Review: {review}
        Result: {result}
        Success: {success}
        ''',
        metadata={
            'review': str(review),
            'success': str(success),
            'result': str(result)[:200],  # Limit to 200 chars for metadata
            'timestamp': datetime.now().isoformat(),
            'type': 'execution'
        }
    )

    try:
        index = get_index()
        if index is not None:
            index.insert(doc)
            print(f"Memory stored: {task_str[:50]}...")
    except Exception as e:
        print(f"Warning: Failed to store memory - {str(e)}")

def retrieve_memory(query):
    # Convert task object to string query if needed
    if not isinstance(query, str):
        # Handle task object
        if hasattr(query, 'title') and hasattr(query, 'description'):
            query_str = f"{query.title} {query.description}"
        else:
            query_str = str(query)
    else:
        query_str = query

    try:
        index = get_index()

        # If index is not available, return default context
        if index is None:
            return "No past experience available yet. This is the first task."

        query_engine = index.as_query_engine(similarity_top_k=3)
        result = query_engine.query(query_str)
        return str(result)
    except Exception as e:
        # Return empty context if query fails
        print(f"Warning: Memory retrieval failed - {str(e)}")
        return f"Unable to retrieve past experience: {str(e)}"

def rank_memory(memory : str):
    """Rank memory based on success status."""
    if 'failed' in memory.lower():
        return 'failed'
    return memory