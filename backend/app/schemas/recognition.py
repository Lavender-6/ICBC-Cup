from datetime import datetime
from typing import Optional

from app.schemas.base import CamelModel


class RecognitionStartRequest(CamelModel):
    dataset_id: str


class RecognitionResultResponse(CamelModel):
    id: str
    dataset_id: str
    modulation: str
    confidence: float
    snr: float
    symbol_rate: Optional[float] = None
    freq_offset: Optional[float] = None
    created_at: datetime


class VisualizationResponse(CamelModel):
    waterfall: list[list[float]]
    constellation: list[dict]
