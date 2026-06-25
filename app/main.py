import time
from fastapi import FastAPI, HTTPException

from app.core.config import settings
from app.database.csv_data import get_user_data
from app.database.vector_db import vector_db
from app.models.schemas import QueryRequest, QueryResponse
from app.services.embedding import get_embedding
from app.services.cache_manager import find_cached_template
from app.services.rag_engine import generate_llm_response

app = FastAPI(title=settings.PROJECT_NAME)


@app.post("/api/v1/query", response_model=QueryResponse)
def query(request: QueryRequest):
    start_time = time.perf_counter()

    # 1. Validate user exists in CSV database
    user_data = get_user_data(request.user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail=f"Customer ID {request.user_id} not found.")

    # 2. Convert query text into an embedding vector
    query_vector = get_embedding(request.text_query)

    # 3. Check semantic cache for a similar query template
    cache_hit = find_cached_template(query_vector)

    if cache_hit:
        # --- CACHE HIT: hydrate the saved template with this user's data ---
        output = cache_hit["template"]

        # Build a mapping from template keys to user's CSV data
        key_mapping = {
            "first_name": user_data.get("First Name", ""),
            "last_name": user_data.get("Last Name", ""),
            "age": user_data.get("Age", ""),
            "city": user_data.get("City", ""),
            "email": user_data.get("Email", ""),
            "account_type": user_data.get("Account Type", ""),
            "account_balance": user_data.get("Account Balance", ""),
            "transaction_type": user_data.get("Transaction Type", ""),
            "transaction_amount": user_data.get("Transaction Amount", ""),
            "balance_after": user_data.get("Account Balance After Transaction", ""),
            "loan_amount": user_data.get("Loan Amount", ""),
            "loan_type": user_data.get("Loan Type", ""),
            "interest_rate": user_data.get("Interest Rate", ""),
            "loan_status": user_data.get("Loan Status", ""),
            "card_type": user_data.get("Card Type", ""),
            "credit_limit": user_data.get("Credit Limit", ""),
            "credit_card_balance": user_data.get("Credit Card Balance", ""),
            "rewards_points": user_data.get("Rewards Points", ""),
            "contact_number": user_data.get("Contact Number", ""),
        }

        for key in cache_hit["required_keys"]:
            placeholder = "{{" + key + "}}"
            if key in key_mapping:
                output = output.replace(placeholder, str(key_mapping[key]))

        latency = (time.perf_counter() - start_time) * 1000
        return QueryResponse(
            status="success",
            source="semantic_cache",
            latency_ms=round(latency, 2),
            output_text=output,
        )

    # --- CACHE MISS: send to Gemini LLM ---
    llm_result = generate_llm_response(request.user_id, request.text_query)

    # Save the template + vector into the cache for future queries
    vector_db.add_record(
        vector=query_vector,
        template=llm_result["reusable_template"],
        required_keys=llm_result["required_keys"],
        concept_id=llm_result["concept_id"],
    )

    latency = (time.perf_counter() - start_time) * 1000
    return QueryResponse(
        status="success",
        source="llm_generation",
        latency_ms=round(latency, 2),
        output_text=llm_result["direct_answer"],
    )