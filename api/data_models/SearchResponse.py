from pydantic import BaseModel
from typing import List, Dict, Any


class SearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
