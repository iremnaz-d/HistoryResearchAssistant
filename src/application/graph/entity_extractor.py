from src.domain.entities.historical_entities.historical_concept import Concept
from src.domain.entities.historical_entities.historical_event import Event
from src.domain.entities.historical_entities.historical_person import Person
from src.domain.entities.historical_entities.historical_place import Place
from src.domain.entities.historical_entities.historical_relationship import Relationship
from src.domain.entities.research_result import ResearchResult
from src.domain.interfaces.llm_client import LLMClientInterface
import json


class EntityExtractor:

    def __init__(self, llm_client: LLMClientInterface):
        self.llm_client = llm_client

    def extract(self, results : list[ResearchResult]):
        full_result = ResearchResult.list_to_text(results) #web search results from search engine

        with open("src/application/prompts/entity_extract.txt", "r", encoding = "utf-8") as f:
            raw_prompt = f.read()

        prompt = raw_prompt.format(provided_sources = full_result)

        structured_json_output = self.llm_client.generate(text = prompt)
        entities_dict = json.loads(structured_json_output)

        entity_list , relation_list= self._map_to_historical_entity(entities_dict)
        return entity_list, relation_list

    @staticmethod
    def _map_to_historical_entity(entities_dict):
        entity_list = []
        relation_list = []

        for key, value in entities_dict.items():
            if key == "persons":
                for entity_dict in value:
                    _id = entity_dict.get("id")
                    _name = entity_dict.get("name")
                    _birth_date = entity_dict.get("birth_date")
                    _death_date = entity_dict.get("death_date")
                    entity_list.append(Person(id = _id, name = _name, birth_date = _birth_date, death_date = _death_date))

            elif key == "events":
                for entity_dict in value:
                    _id = entity_dict.get("id")
                    _name = entity_dict.get("name")
                    _start_date = entity_dict.get("start_date")
                    _end_date = entity_dict.get("end_date")
                    _description = entity_dict.get("description")
                    entity_list.append(Event(id=_id, name=_name, start_date=_start_date, end_date=_end_date, description = _description))

            elif key == "places":
                for entity_dict in value:
                    _id = entity_dict.get("id")
                    _name = entity_dict.get("name")
                    _type = entity_dict.get("type")
                    entity_list.append(Place(id = _id, name = _name, type = _type))

            elif key == "concepts":
                for entity_dict in value:
                    _id = entity_dict.get("id")
                    _name = entity_dict.get("name")
                    entity_list.append(Concept(id = _id, name = _name))

            elif key == "relationships":
                for entity_dict in value:
                    _source_id = entity_dict.get("source_id")
                    _target_id = entity_dict.get("target_id")
                    _type = entity_dict.get("type")
                    _evidence_url = entity_dict.get("evidence_url")
                    relation_list.append(Relationship(source_id = _source_id, target_id = _target_id, type = _type, evidence_url = _evidence_url))

            else:
                raise ValueError("LLM's Json Structured Output is wrong")

        return entity_list, relation_list