from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Enterprise(Base):
    __tablename__ = "enterprises"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=False)
    stage = Column(String(50), nullable=False, default="立项")
    description = Column(Text)
    founded_year = Column(Integer)
    employee_count = Column(Integer)
    rd_ratio = Column(Float, default=0.0)
    base_valuation = Column(Float, default=0.0)
    current_valuation = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
