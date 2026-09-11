from pydantic import BaseModel
from datetime import datetime


class DatasetBase(BaseModel):
    name: str
    format: str
    size: int


class DatasetResponse(BaseModel):
    id: str
    name: str
    format: str
    size: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
