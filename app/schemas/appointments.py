from datetime import datetime
from pydantic import Field, BaseModel

class AppointmentRequest(BaseModel):
    doctor_id: str = Field(..., description="Doctor ID")
    appointment_time: datetime = Field(..., description="Appointment time (e.g., '17:00:00')")

class RescheduleAppointment(BaseModel):
    appointment_id: str = Field(..., description="Appointment ID")
    appointment_time: datetime = Field(..., description="Appointment time (e.g., '17:00:00')")
