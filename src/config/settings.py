from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    exa_api_key : str
    gemini_api_key : str
    groq_api_key : str

    GEMINI_MODEL_NAME : str = "gemini-3.6-flash"
    GROQ_MODEL_NAME : str = "llama-3.3-70b-versatile"

    MAX_SEARCH_RESULTS : int = 5 #web search

    GRAPH_DB_PATH : str = str(Path(__file__).resolve().parent.parent.parent / "graph_db")
    VECTOR_DB_PATH : str = str(Path(__file__).resolve().parent.parent.parent / "vector_db")



    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = False
    )

