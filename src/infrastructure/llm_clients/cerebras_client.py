from src.config.settings import Settings
from src.domain.interfaces.llm_client import LLMClientInterface
from cerebras.cloud.sdk import Cerebras


class CerebrasClient(LLMClientInterface):

    def __init__(self, provided_api_key = None):
        self.settings = Settings()
        api_key = self.settings.cerebras_api_key or provided_api_key

        if not api_key:
            self.client = None
        else:
            self.client = Cerebras(api_key = api_key)

    def generate(self, text, tools = None, history = None):
        if self.client is None:
            raise ValueError("Cerebras API Key not found.")

        response = self.client.completions.create(
            prompt = text,
            model = self.settings.CEREBRAS_MODEL_NAME
        )

        return response

