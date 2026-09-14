from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


MILESTONE_STAGES = [
    "立项预研",
    "原型验证",
    "流片成功",
    "商业化量产",
    "上市预备",
]


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(String(36), primary_key=True, index=True)
    enterprise_id = Column(String(36), ForeignKey("enterprises.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    stage = Column(String(50), nullable=False)
    description = Column(Text)
    expected_date = Column(DateTime)
    actual_date = Column(DateTime)
    progress = Column(Float, default=0.0)
    status = Column(String(20), default="pending")
    is_verified = Column(Boolean, default=False)
    audit_report = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class FinancialTool(Base):
    __tablename__ = "financial_tools"

    id = Column(String(36), primary_key=True, index=True)
    milestone_id = Column(String(36), ForeignKey("milestones.id"), nullable=False, index=True)
    tool_type = Column(String(100), nullable=False)
    tool_name = Column(String(200), nullable=False)
    amount = Column(Float, default=0.0)
    conditions = Column(Text)
    is_triggered = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
