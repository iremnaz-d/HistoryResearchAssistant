from sentence_transformers import SentenceTransformer

from src.domain.interfaces.embedding_model import EmbeddingModelInterface


class BgeEmbedding(EmbeddingModelInterface):
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-m3")

    def embed(self, text:str):
        return self.model.encode(text).tolist()

