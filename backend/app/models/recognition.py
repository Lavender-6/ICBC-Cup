from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class RecognitionRecord(Base):
    __tablename__ = "recognition_records"

    id = Column(String(36), primary_key=True, index=True)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    modulation = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    snr = Column(Float, nullable=False)
    symbol_rate = Column(Float, nullable=True)
    freq_offset = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
