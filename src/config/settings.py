from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    exa_api_key : str
    gemini_api_key : str
    gemini_model_name : str


    model_config = SettingsConfigDict(env_file = ".env")

