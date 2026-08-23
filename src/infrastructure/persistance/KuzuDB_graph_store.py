import kuzu
from src.config.settings import Settings
from src.domain.entities.historical_entities.historical_concept import Concept
from src.domain.entities.historical_entities.historical_event import Event
from src.domain.entities.historical_entities.historical_person import Person
from src.domain.entities.historical_entities.historical_place import Place
from src.domain.interfaces.graph_store import GraphStoreInterface


class KuzuDB(GraphStoreInterface):

    def __init__(self):
        settings = Settings()
        db = kuzu.Database(settings.GRAPH_DB_PATH)
        self.conn = kuzu.Connection(db)
        self._setup_schema()

    def _setup_schema(self):
        self.conn.execute(
            "CREATE NODE TABLE IF NOT EXISTS Person (id STRING, name STRING, birth_date DATE, death_date DATE, PRIMARY KEY (id))"
        )

        self.conn.execute(
            "CREATE NODE TABLE IF NOT EXISTS Event (id STRING, name STRING, start_date DATE, end_date DATE, description STRING, PRIMARY KEY (id))"
        )

        self.conn.execute(
            "CREATE NODE TABLE IF NOT EXISTS Place (id STRING, name STRING, type STRING, PRIMARY KEY (id))"
        )

        self.conn.execute(
            "CREATE NODE TABLE IF NOT EXISTS Concept (id STRING, name STRING, PRIMARY KEY (id))"
        )

    def add_entity(self, entity):

        if isinstance(entity, Person):

            query = """
            MERGE (p:Person {id: $id})
            ON CREATE SET p.name = $name, p.birth_date = $birth_date, p.death_date = $death_date
            """

            params = {
                "id": entity.id,
                "name": entity.name,
                "birth_date": entity.birth_date.strftime("%Y-%m-%d") if entity.birth_date else None,
                "death_date": entity.death_date.strftime("%Y-%m-%d") if entity.death_date else None
            }

            self.conn.execute(query, parameters = params)

        elif isinstance(entity, Event):

            query = """
            MERGE (e:Event {id: $id})
            ON CREATE SET e.name = $name, e.start_date = $start_date, e.end_date = $end_date, e.description = $description
            """

            params = {
                "id": entity.id,
                "name": entity.name,
                "start_date": entity.start_date.strftime("%Y-%m-%d") if entity.start_date else None,
                "end_date": entity.end_date.strftime("%Y-%m-%d") if entity.end_date else None,
                "description": entity.description if entity.description else None
            }

            self.conn.execute(query, parameters = params)

        elif isinstance(entity, Place):

            query = """
            MERGE (p:Place {id: $id})
            ON CREATE SET p.name = $name, p.type = $type
            """

            params = {
                "id": entity.id,
                "name": entity.name,
                "type": entity.type if entity.type else None
            }

            self.conn.execute(query, parameters = params)

        elif isinstance(entity, Concept):

            query = """
            MERGE (c:Concept {id: $id})
            ON CREATE SET c.name = $name
            """

            params = {
                "id": entity.id,
                "name": entity.name
            }

            self.conn.execute(query, parameters = params)

        else:
            raise ValueError("Invalid Entity Type")

    def add_relation(self,source, target, relation_type):
        source_label = source.__class__.__name__
        target_label = target.__class__.__name__

        ddl_query = f"CREATE REL TABLE IF NOT EXISTS {relation_type} (FROM {source_label} TO {target_label})"
        try:
            self.conn.execute(ddl_query)
        except RuntimeError:
            pass

        query = f"""
        MATCH (src:{source_label}{{id: $source_id}}), (tgt:{target_label}{{id: $target_id}})
        MERGE (src)-[r:{relation_type}]->(tgt)
        """

        params = {
            "source_id" : source.id,
            "target_id" : target.id
        }

        self.conn.execute(query, parameters = params)

    def query_graph(self, entity):
        entity_label = entity.__class__.__name__

        query = f"""
        MATCH (src:{entity_label}  {{id: $id}})-[r]->(tgt)
        RETURN r,tgt
        """

        results = self.conn.execute(query, parameters = {"id": entity.id})

        result_list = []
        while results.has_next():
            row = results.get_next()
            rel = row[0]
            tgt = row[1]

            target_data = dict(tgt)

            target_id = target_data.pop("id", None)
            target_label = target_data.pop("_label", None)

            result_list.append({
                "relation_type": rel.get("_label", ""),
                "target_id": target_id,
                "target_type": target_label,
                "target_properties": target_data  # name, start_date, type, description etc.
            })

        return result_list
