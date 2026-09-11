from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    format = Column(String(10), nullable=False)
    size = Column(Integer, nullable=False)
    file_path = Column(String(512), nullable=False)
    status = Column(String(20), default="uploaded")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
