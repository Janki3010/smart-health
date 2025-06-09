from fastapi import HTTPException

from app.models.appointment import AppointmentStatus
from app.repository.appointment_repository import AppointmentRepository
from app.schemas.appointments import AppointmentRequest

class AppointmentService:
    def __init__(self):
        self.appointment_repository = AppointmentRepository()

    def book_appointment(self, patient_id: str, appointment_request: AppointmentRequest):
        return self.appointment_repository.create_appointment(patient_id, appointment_request)

    def cancel_appointment(self, appointment_id: str):
        appointment = self.appointment_repository.get_appointment(appointment_id)

        if not appointment:
            raise HTTPException(status_code=401, detail="Appointment doesn't exists")

        return self.appointment_repository.cancel_appointment(appointment_id)

    def update_appointment_status(self, appointment_id: str, status: AppointmentStatus):
        return self.appointment_repository.update_status(appointment_id, status)

    def get_your_appointments(self, user_id: str):
        return self.appointment_repository.get_appointment_history(user_id)

    def get_all_appointments(self, doc_id: str):
        return self.appointment_repository.get_appointments(doc_id)