import json
import time
from typing import Dict, Any
from pydantic import BaseModel, Field
from google import genai

from app.core.config import settings
from app.database.csv_data import get_user_data
from app.services.prompts import SYSTEM_PROMPT

_client = genai.Client(api_key=settings.GEMINI_API_KEY)


class LLMResponse(BaseModel):
    # schema for gemini output
    direct_answer: str = Field(description="A personalized response for this user.")
    reusable_template: str = Field(description="Generic template with {{placeholder}} tags.")
    required_keys: list[str] = Field(description="List of placeholder names used in the template.")


def generate_llm_response(user_id: int, query_text: str) -> Dict[str, Any]:
    """
    Fetch user data from CSV, send it to Gemini along with the query,
    and return the structured response (direct answer + reusable template).
    """
    #Get user data
    user_data = get_user_data(user_id)

    #build context for llm
    context = {
        "user_profile": {
            "first_name": user_data["First Name"],
            "last_name": user_data["Last Name"],
            "age": user_data["Age"],
            "city": user_data["City"],
            "email": user_data["Email"],
            "account_type": user_data["Account Type"],
            "account_balance": user_data["Account Balance"],
        },
        "latest_transaction": {
            "transaction_type": user_data["Transaction Type"],
            "transaction_amount": user_data["Transaction Amount"],
            "balance_after": user_data["Account Balance After Transaction"],
        },
        "loan_info": {
            "loan_amount": user_data["Loan Amount"],
            "loan_type": user_data["Loan Type"],
            "interest_rate": user_data["Interest Rate"],
            "loan_status": user_data["Loan Status"],
        },
        "card_info": {
            "card_type": user_data["Card Type"],
            "credit_limit": user_data["Credit Limit"],
            "credit_card_balance": user_data["Credit Card Balance"],
            "rewards_points": user_data["Rewards Points"],
        },
    }

    prompt = f"User Query: {query_text}\nDatabase Context: {json.dumps(context)}"

    #3 call gemini
    response = _client.models.generate_content(
        model=settings.LLM_MODEL,
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
            "response_schema": LLMResponse,
        },
    )

    #4. return
    payload = json.loads(response.text)
    payload["concept_id"] = f"gemini_{int(time.time())}"
    return payload
