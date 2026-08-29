import os

from src.domain.entities.historical_entities.historical_place import Place

os.environ["EXA_API_KEY"] = "dummy_key"
os.environ["GEMINI_API_KEY"] = "dummy_key"
os.environ["GROQ_API_KEY"] = "dummy_key"


from datetime import datetime
from src.domain.entities.historical_entities.historical_person import Person
from src.infrastructure.persistance.KuzuDB_graph_store import KuzuDB

db = KuzuDB()

test_person = Person(
    id="ataturk",
    name="Mustafa Kemal Atatürk",
    birth_date=datetime(1881, 1, 1),
    death_date=datetime(1938, 11, 10)
)

test_place = Place(
    id="turkiye_cumhuriyeti",
    name="Türkiye Cumhuriyeti",
    type="COUNTRY"
)

print("Adding entities to database...")
db.add_entity(test_person)
db.add_entity(test_place)
print("Successful!")

print("Adding relations to database...")
db.add_relation(
source=test_person,
    target=test_place,
    relation_type="FOUNDED",
    evidence_url="https://tr.wikipedia.org/wiki/Türkiye"
)
print("Successful")

print("\nSearching")
result_list = db.query_graph(test_person)
print(result_list)
print("Successful")