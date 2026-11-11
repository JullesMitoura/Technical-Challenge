from datetime import datetime
from pydantic import BaseModel


class TextRequest(BaseModel):
    text: str


class TextResponse(BaseModel):
    letter_count: int


class HistoryRecord(BaseModel):
    text: str
    letter_count: int
    created_at: datetime = datetime.now()