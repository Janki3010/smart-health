from sqlalchemy import Column, String, Time
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import BaseModel

class Doctor(BaseModel):
    __tablename__ = "doctors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    specialization = Column(String, nullable=False)
    qualifications = Column(String)
    available_days = Column(String)  # e.g., "Mon,Tue,Wed"
    available_from = Column(Time)
    available_to = Column(Time)


