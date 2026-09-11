from datetime import datetime

from app.schemas.base import CamelModel


class DatasetBase(CamelModel):
    name: str
    format: str
    size: int


class DatasetResponse(CamelModel):
    id: str
    name: str
    format: str
    size: int
    status: str
    created_at: datetime
