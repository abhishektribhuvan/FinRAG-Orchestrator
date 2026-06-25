import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Personalized Semantic Cache & RAG Engine"

    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LLM_MODEL: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "gemini-embedding-001"

    # Data
    CSV_PATH: str = str(Path(__file__).resolve().parent.parent / "database" / "Comprehensive_Banking_Database.csv")

    # Semantic cache similarity threshold (0.0 to 1.0)
    SIMILARITY_THRESHOLD: float = 0.92

settings = Settings()