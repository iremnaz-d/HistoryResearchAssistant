from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    exa_api_key : str
    gemini_api_key : str
    GEMINI_MODEL_NAME : str = "gemini-3.6-flash"
    MAX_SEARCH_RESULTS : int = 5


    model_config = SettingsConfigDict(env_file = ".env")

