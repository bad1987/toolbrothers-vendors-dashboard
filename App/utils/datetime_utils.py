
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, Query

def validate_start_time(start_time: Optional[str] = Query(None, description="The start date of the range to search for orders (inclusive). Format: YYYY-MM-DD")) -> Optional[datetime]:
    if start_time is not None:
        try:
            return datetime.strptime(start_time, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid start_time. Expected format: %Y-%m-%d")
    return None

def validate_end_time(end_time: Optional[str] = Query(None, description="The end date of the range to search for orders (inclusive). Format: YYYY-MM-DD")) -> Optional[datetime]:
    if end_time is not None:
        try:
            return datetime.strptime(end_time, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid end_time. Expected format: %Y-%m-%d")
    return None