from src.config.settings import Settings
from src.domain.interfaces.llm_client import LLMClientInterface
import cohere
from cohere.types import UserChatMessageV2


class CohereClient(LLMClientInterface):

    def __init__(self, provided_api_key = None):
        self.settings = Settings()
        api_key = self.settings.cohere_api_key or provided_api_key

        if not api_key:
            self.client = None
        else:
            self.client = cohere.ClientV2(api_key = api_key)

    def generate(self, text, history = None, tools = None):

        print("Using Cohere Client...")

        if self.client is None:
            raise ValueError("Cohere API Key not found")

        response = self.client.chat(
            model = self.settings.COHERE_MODEL_NAME,
            messages = [UserChatMessageV2(role = "user", content = text)]
        )

        final_text = "".join([item.text for item in response.message.content if item.type == "text"])
        return final_text
