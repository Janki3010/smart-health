from app.models.appointment import Appointment, AppointmentStatus
from app.repository.base_repository import BaseRepository
from app.schemas.appointments import AppointmentRequest, RescheduleAppointment


class AppointmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Appointment)

    def create_appointment(self, patient_id: str, appointment_request: AppointmentRequest):
        db_create = Appointment(
            patient_id=patient_id,
            doctor_id=appointment_request.doctor_id,
            appointment_time=appointment_request.appointment_time
        )
        return self.save(db_create)

    def get_appointment(self, appointment_id: str):
        return self.get_by_id(appointment_id)

    def cancel_appointment(self, appointment_id: str):
        return self.update_by_id(appointment_id, {"status": AppointmentStatus.CANCELLED})

    def update_status(self, appointment_id: str, status: AppointmentStatus):
        return self.update_by_id(appointment_id, {"status": status})

    def get_appointments(self, app_id):
        return self.get_by_id({'id': app_id})

    def get_appointment_history(self, id: str):
        return self.get_all({'patient_id': id})

    def get_appointments_doc(self, doc_id: str):
        return self.get_all({'doctor_id': doc_id})

    def update_appointment_time(self, reschedule_request: RescheduleAppointment):
        return self.update_by_id(reschedule_request.appointment_id, {"appointment_time": reschedule_request.appointment_time, "status": AppointmentStatus.PENDING})
