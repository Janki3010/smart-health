from sqlalchemy import Column, DateTime, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid

from app.models.base import BaseModel

class AppointmentStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Appointment(BaseModel):
    __tablename__ = "appointments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    appointment_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING)

