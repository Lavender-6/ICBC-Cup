from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(String(36), primary_key=True, index=True)
    enterprise_id = Column(String(36), ForeignKey("enterprises.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100))
    education = Column(String(200))
    is_founder = Column(Boolean, default=False)
    paper_count = Column(Integer, default=0)
    citation_count = Column(Integer, default=0)
    h_index = Column(Integer, default=0)
    patent_count = Column(Integer, default=0)
    experience_years = Column(Integer, default=0)
    portrait_score = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
