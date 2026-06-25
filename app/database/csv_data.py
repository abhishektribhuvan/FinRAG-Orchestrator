import pandas as pd
from typing import Optional
from app.core.config import settings

# Load the CSV into memory once at import time
_df = pd.read_csv(settings.CSV_PATH)


def get_user_data(customer_id: int) -> Optional[dict]:
    """Look up a customer by 'Customer ID' and return all their data as a dict."""
    row = _df[_df["Customer ID"] == customer_id]
    if row.empty:
        return None
    return row.iloc[0].to_dict()
