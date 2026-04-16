from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from qdrant_client import QdrantClient
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

client = QdrantClient(host='127.0.0.1', port=6333)
COLLECTION_NAME = 'agent_memory'

# Initialize embeddings
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

# Initialize vector store
vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Initialize index globally
index = None

def get_index():
    """Get or create the vector store index."""
    global index
    if index is None:
        try:
            index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
                embed_model=embed_model
            )
        except Exception as e:
            print(f"Error initializing index: {e}")
            # Return a safe fallback
            return None
    return index