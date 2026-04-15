import time
from langchain_ollama import ChatOllama
import logging
from langchain_core.messages import HumanMessage
from app.core.config import LlmConfig

logger = logging.getLogger("llm_service")
logging.basicConfig(level=logging.INFO)

class LlmClient:
    def __init__(self, config: LlmConfig):
        self.config = config
        self.chat_ollama = ChatOllama(model = config.model,temperature = config.temp)

    def invoke(self,prompt : str):
        start_time = time.time()

        response = self.chat_ollama.invoke([HumanMessage(content=prompt)])

        duration = time.time() - start_time

        logger.info('llm call',extra={
            'model': self.config.model,
            'latency':round(duration, 3)
        })

        return response.content
