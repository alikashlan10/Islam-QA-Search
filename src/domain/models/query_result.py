from pydantic import BaseModel
from typing import List


class RetrievalSource(BaseModel):
    video_id:      str
    chunk:         str
    title:         str
    thumbnail_url: str
    chunk_index:   int


class RetrievalResult(BaseModel):
    answer:  str
    sources: List[RetrievalSource]

