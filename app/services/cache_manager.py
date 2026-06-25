import numpy as np
from typing import Dict, Any, Optional
from app.core.config import settings
from app.database.vector_db import vector_db


def _cosine_similarity(vec1: list, vec2: list) -> float:
    """Compute cosine similarity between two vectors."""
    v1, v2 = np.array(vec1), np.array(vec2)
    norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (norm1 * norm2))


def find_cached_template(query_vector: list) -> Optional[Dict[str, Any]]:
    """Search the vector DB for a template whose embedding is similar enough to the query."""
    best_match = None
    best_score = 0.0

    for record in vector_db.get_all():
        score = _cosine_similarity(query_vector, record["vector"])
        if score > best_score:
            best_score = score
            best_match = record

    if best_match and best_score >= settings.SIMILARITY_THRESHOLD:
        return best_match

    return None