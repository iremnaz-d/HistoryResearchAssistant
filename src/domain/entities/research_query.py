from pydantic import BaseModel
from typing import Optional
from googletrans import Translator
import asyncio

class Query(BaseModel):
    """
    Kullanıcının sorusunu temsil eden basit model.
    """

    raw_query: str
    research_question : Optional[str] = None
    language : Optional[str] = None


    def __init__(self, raw_query):
        self.raw_query , self.language = asyncio.run(self.translate_to_english(raw_query))
        self.research_question = self.raw_query #bunu Exa zaten semantic arama yaptığı için böyle yaptım, başka bir search enginede değiştirilebilir


    @staticmethod
    async def translate_to_english(text):
        translator = Translator()

        detection  = await translator.detect(text)

        if detection.lang == "en":
            return text

        translated_text = await translator.translate(text, src=detection.lang, dest='en')
        return translated_text.text, detection.lang





