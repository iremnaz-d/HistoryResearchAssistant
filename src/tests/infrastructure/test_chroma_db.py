import os

from src.domain.entities.document import Document
from src.infrastructure.embeddings.BGE_M3_embedding_model import BgeEmbedding
from src.infrastructure.persistance.ChromaDB_vector_store import ChromaDB

os.environ["EXA_API_KEY"] = "dummy_key"
os.environ["GEMINI_API_KEY"] = "dummy_key"
os.environ["GROQ_API_KEY"] = "dummy_key"

d1 = Document(id = "1", text = "jshfskdhfjksdfhkdshfsdkjfdshfdskjf", source = "https://example.com")
d2 = Document(id = "2", text = "sjfkhwpojwvnksğjhfıerbvwepovj", source = "https://example.com")
d3 = Document(id = "3",
              text = "Atatürk Türkiye'nin ilk cumhurbaşkanıdır.",
              source = "https://example.com")

document_list = [d1,d2,d3]

bge_embedding = BgeEmbedding()
chroma_db = ChromaDB(embedding_model = bge_embedding)

print("Adding to database...")
chroma_db.add_documents(document_list)
print("Successful!")

print("\nSearching")
doc_list = chroma_db.search(query = "Atatürk")
print(doc_list)
print("Successful")