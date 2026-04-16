from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from qdrant_client import QdrantClient
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

client = QdrantClient(host='127.0.0.1', port=6333)
COLLECTION_NAME = 'agent_memory'

vector_store = QdrantVectorStore(client = client,collection_name= COLLECTION_NAME)
embed_model = HuggingFaceEmbedding("BAAI/bge-small-en")

storage_context = StorageContext.from_defaults(vector_store=vector_store)
vector_store_index = VectorStoreIndex.from_vector_store(vector_store = vector_store, embed_model=embed_model)