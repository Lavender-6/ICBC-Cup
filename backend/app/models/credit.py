from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class CreditRecord(Base):
    __tablename__ = "credit_records"

    id = Column(String(36), primary_key=True, index=True)
    enterprise_id = Column(String(36), ForeignKey("enterprises.id"), nullable=False, index=True)
    milestone_id = Column(String(36), ForeignKey("milestones.id"), nullable=True)
    base_amount = Column(Float, default=0.0)
    progress_factor = Column(Float, default=0.0)
    risk_factor = Column(Float, default=1.0)
    final_amount = Column(Float, default=0.0)
    status = Column(String(20), default="active")
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id = Column(String(36), primary_key=True, index=True)
    enterprise_id = Column(String(36), ForeignKey("enterprises.id"), nullable=False, index=True)
    alert_type = Column(String(100), nullable=False)
    severity = Column(String(20), default="warning")
    message = Column(Text, nullable=False)
    is_resolved = Column(String(10), default="0")
    created_at = Column(DateTime, server_default=func.now())
