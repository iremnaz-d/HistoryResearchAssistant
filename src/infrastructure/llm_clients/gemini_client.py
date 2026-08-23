from src.config.settings import Settings
from src.domain.interfaces.llm_client import LLMClientInterface
from google import genai


class GeminiClient(LLMClientInterface):

    def __init__(self, provided_api_key=None):
        self.settings = Settings()
        api_key = self.settings.gemini_api_key or provided_api_key

        if not api_key:
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)


    def generate(self, text, tools=None, history=None): # toolsu daha kullanmadım
        if self.client is None:
            raise ValueError("Gemini API Key not found.")

        gemini_history = []

        if history:
            for message in history:
                gemini_history.append(
                    {"role":message['role'], "parts": [{"text": message['content']}]}
                )

        gemini_history.append(
            {"role": "user", "parts": [{"text": text}]}
        )


        response = self.client.models.generate_content(
            model = self.settings.GEMINI_MODEL_NAME,
            contents = gemini_history
        )

        return response