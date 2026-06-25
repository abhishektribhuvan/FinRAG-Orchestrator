from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    user_id: int = Field(..., example=1, description="Customer ID from the banking database")
    text_query: str = Field(..., example="What is my account balance?")


class QueryResponse(BaseModel):
    status: str
    source: str
    latency_ms: float
    output_text: str