from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Patent(Base):
    __tablename__ = "patents"

    id = Column(String(36), primary_key=True, index=True)
    enterprise_id = Column(String(36), ForeignKey("enterprises.id"), nullable=False, index=True)
    patent_number = Column(String(50), nullable=False)
    title = Column(String(500))
    ipc_class = Column(String(50))
    cited_count = Column(Integer, default=0)
    cites_count = Column(Integer, default=0)
    family_size = Column(Integer, default=1)
    has_international = Column(Boolean, default=False)
    litigation_risk = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    filed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())


class PatentCitation(Base):
    __tablename__ = "patent_citations"

    id = Column(Integer, primary_key=True, index=True)
    source_patent_id = Column(String(36), ForeignKey("patents.id"), nullable=False)
    target_patent_id = Column(String(36), ForeignKey("patents.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
