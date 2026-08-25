from src.config.settings import Settings
from src.domain.entities.document import Document
from src.domain.interfaces.embedding_service import EmbeddingModelInterface
from src.domain.interfaces.vector_store import VectorStoreInterface
import chromadb


class ChromaDB(VectorStoreInterface):

    def __init__(self, embedding_model : EmbeddingModelInterface):
        self.embedding_model = embedding_model
        self.settings = Settings()
        client = chromadb.PersistentClient(self.settings.VECTOR_DB_PATH)
        self.collection = client.get_or_create_collection(name = "Documents")

    def add_documents(self, documents: list[Document]):
        texts = []
        sources = []
        ids = []
        embeddings = []
        for document in documents:
            texts.append(document.text)
            sources.append({"source":document.source} if document.source else {"source":None})
            ids.append(document.id)
            embeddings.append(self.embedding_model.embed(text = document.text))

        self.collection.add(documents = texts, metadatas = sources, ids = ids, embeddings = embeddings)

    def search(self, query: str):
        query_embedding = self.embedding_model.embed(text = query)

        results = self.collection.query(
            query_embeddings = query_embedding,
            n_results = self.settings.MAX_SEARCH_RESULTS
        )

        document_list = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                doc = Document(
                    id=results["ids"][0][i],
                    text=results["documents"][0][i],
                    source=results["metadatas"][0][i].get("source")
                )
                document_list.append(doc)

        return document_list