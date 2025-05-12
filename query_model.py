from pydantic import BaseModel
from typing import List

class Query(BaseModel):
    condition: str
    allergies: List[str]
