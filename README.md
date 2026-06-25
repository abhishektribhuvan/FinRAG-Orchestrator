# Personalized Semantic Cache & RAG Engine

A FastAPI-based banking query system that uses **Gemini AI** for intelligent responses and a **semantic vector cache** for fast repeated queries.

## How It Works

```
User Query → Gemini Embedding → Vector Similarity Search
                                        │
                          ┌──────────────┴──────────────┐
                     Cache HIT                     Cache MISS
                          │                              │
               Fill template with               Send query + user data
               user's CSV data                     to Gemini LLM
                          │                              │
                   Return fast                  Return LLM answer +
                   response                     save template to cache
```

1. **User sends a query** with their `user_id` (Customer ID) and `text_query`
2. The query is **converted to a vector** using Gemini's embedding model
3. The system **searches the vector cache** for a similar previously-answered query
4. **If found (cache hit)**: The saved template is filled with the user's data from the CSV → instant response
5. **If not found (cache miss)**: The query + user data is sent to **Gemini LLM**, which generates a personalized answer and a reusable template. The template is saved to the cache for future queries.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key (optional — a default is provided)
set GEMINI_API_KEY=your_api_key_here

# Start the server
uvicorn app.main:app --reload
```

## API Usage

**POST** `/api/v1/query`

```json
{
  "user_id": 55,
  "text_query": "What is my account balance?"
}
```

**Response:**
```json
{
  "status": "success",
  "source": "llm_generation",
  "latency_ms": 1523.45,
  "output_text": "Hi John, your Current account balance is 5639.51."
}
```

On the second similar query, the response comes from `semantic_cache` with much lower latency about 1000x lower response time.
**Response:**
```json
{
  "status": "success",
  "source": "semantic_cache",
  "latency_ms": 1.27,
  "output_text": "Hi John, your Savings account balance is 5639.51."
}
```


## Project Structure

```
app/
├── main.py                 # FastAPI app & query endpoint
├── core/
│   └── config.py           # Settings (API keys, thresholds, paths)
├── database/
│   ├── csv_data.py          # CSV reader (Comprehensive_Banking_Database.csv)
│   └── vector_db.py         # In-memory vector store for cached templates
├── models/
│   └── schemas.py           # Request/Response Pydantic models
└── services/
    ├── embedding.py         # Gemini embedding API
    ├── cache_manager.py     # Cosine similarity search
    ├── rag_engine.py        # Gemini LLM call with user context
    └── prompts.py           # System prompt for Gemini
```

## Data

The system reads user data from `app/database/Comprehensive_Banking_Database.csv` which contains 5000+ banking customers with account details, transactions, loans, and credit card information.
