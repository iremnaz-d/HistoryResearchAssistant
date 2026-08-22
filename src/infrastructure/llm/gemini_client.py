from src.config.settings import Settings
from src.domain.interfaces.llm_client import LLMClientInterface
from google import genai
from google.genai import types


class GeminiClient(LLMClientInterface):

    def __init__(self, provided_api_key=None):
        api_key = Settings.gemini_api_key or provided_api_key

        if not api_key:
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)


    def generate(self, text, tools=None, history=None): # toolsu daha kullanmadım
        if self.client is None:
            raise ValueError("Gemini API Key not found.")

        if history is None:
            history = [text]

        else:
            history.append(text)

        response = self.client.models.generate_content(
            model = Settings.GEMINI_MODEL_NAME,
            contents = history
        )

        return response