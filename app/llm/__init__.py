from app.llm.llm_service import LlmService, LlmConfig, LlmClient

_config = LlmConfig()
_client = LlmClient(_config)
llm_service = LlmService(_client)

def generate(prompt:str) -> str:
    return llm_service.generate(prompt)