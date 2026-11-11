from datetime import datetime
from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str


class TextResponse(BaseModel):
    letter_count: int


class HistoryRecord(BaseModel):
    text: str
    letter_count: int
    created_at: datetime = Field(default_factory=datetime.now)
