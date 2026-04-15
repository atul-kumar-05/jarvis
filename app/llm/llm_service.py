import time
from app.llm.llm_client import LlmClient, LlmConfig, logger
from app.llm.llm_exception import LLMError

class LlmService:
    def __init__(self,llm : LlmClient):
        self.client = llm

    def generate(self, prompt:str) -> str:
        last_exception = None
        max_retries = self.client.config.max_retries

        for i in range(max_retries):
            try:
                return self.client.invoke(prompt)
            except Exception as e:
                last_exception = e
                logger.warning('llm entry',extra={
                    'attempt': i+1,
                    'exception': last_exception
                })
                time.sleep(2** i)

        detail = str(last_exception) if last_exception else "unknown error"
        raise LLMError(
            f"LLM generation failed after {max_retries} retries: {detail}"
        ) from last_exception
