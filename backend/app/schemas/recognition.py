from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RecognitionStartRequest(BaseModel):
    dataset_id: str


class RecognitionResultResponse(BaseModel):
    id: str
    dataset_id: str
    modulation: str
    confidence: float
    snr: float
    symbol_rate: Optional[float] = None
    freq_offset: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class VisualizationResponse(BaseModel):
    waterfall: list[list[float]]
    constellation: list[dict]
