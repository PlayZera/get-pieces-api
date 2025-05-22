from typing import Optional
from openai import BaseModel

class SearchResult(BaseModel):
    link: str
    title: Optional[str]
    snippet: Optional[str]