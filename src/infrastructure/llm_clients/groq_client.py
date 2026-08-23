from src.config.settings import Settings
from src.domain.interfaces.llm_client import LLMClientInterface
from groq import Groq


class GroqClient(LLMClientInterface):

    def __init__(self, provided_api_key=None):
        self.settings = Settings()
        api_key = self.settings.openai_api_key or provided_api_key

        if not api_key:
            self.client = None
        else:
            self.client = Groq(api_key = api_key)



    def generate(self, text, tools = None, history = None):
        if self.client is None:
            raise ValueError("Groq API Key is not found.")

        if not history:
            history = []

        else:
            history.append({"role":"user", "content": text})

        response = self.client.chat.completions.create(
            model = self.settings.GROQ_MODEL_NAME,
            messages = history
        )

        return response.choices[0].message.content