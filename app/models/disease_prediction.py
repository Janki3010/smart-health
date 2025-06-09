from sqlalchemy import Column, ForeignKey, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.models.base import BaseModel


class DiseasePrediction(BaseModel):
    __tablename__ = "disease_predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    symptoms = Column(String, nullable=False)  # comma-separated list
    predicted_disease = Column(String, nullable=False)

