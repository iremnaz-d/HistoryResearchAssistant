from pydantic import BaseModel, HttpUrl

class Document(BaseModel):
    id : str
    text : str
    source : HttpUrl | None = None

    @staticmethod
    def list_to_text(documents: list["Document"]):
        s = ""
        for document in documents:
            s += str(document.source) + "\n" + document.text + "\n\n"

        return s