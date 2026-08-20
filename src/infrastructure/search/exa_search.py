import os
from exa_py import Exa

from src.config.settings import Settings
from src.domain.interfaces.search_engine import SearchEngineInterface


class ExaSearchEngine(SearchEngineInterface):

    def __init__(self):
        settings = Settings()


    def search(self):
        pass