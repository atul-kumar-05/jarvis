from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.llm = Ollama(
    model="tinyllama",
    request_timeout=60.0
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en"
)