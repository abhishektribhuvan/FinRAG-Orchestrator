from typing import List
from google import genai
from app.core.config import settings

_client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Cache: exact query text → embedding vector (deterministic, safe to cache forever)
_embedding_cache: dict[str, List[float]] = {}


def get_embedding(text: str) -> List[float]:
    """Convert text into a 768-dimensional vector using Gemini's embedding model.
    Returns cached result if the same text was embedded before."""
    if text in _embedding_cache:
        return _embedding_cache[text]

    result = _client.models.embed_content(
        model=settings.EMBEDDING_MODEL,
        contents=text,
    )
    vector = result.embeddings[0].values
    _embedding_cache[text] = vector
    return vector