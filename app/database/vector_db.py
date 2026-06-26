from typing import List, Dict, Any, Optional


class VectorDB:
    def __init__(self):
        self.collection: List[Dict[str, Any]] = []

    def add_record(self, vector: List[float], template: str, required_keys: List[str], concept_id: str):

        self.collection.append({
            "concept_id": concept_id,
            "vector": vector,
            "template": template,
            "required_keys": required_keys,
        })

    def get_all(self) -> List[Dict[str, Any]]:
        #Return all stored records for similarity search.
        return self.collection


vector_db = VectorDB()
