from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.models.base import BaseModel


class MedicalReport(BaseModel):
    __tablename__ = "medical_reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)