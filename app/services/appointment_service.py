from fastapi import HTTPException, BackgroundTasks

from app.models.appointment import AppointmentStatus
from app.repository.appointment_repository import AppointmentRepository
from app.repository.authentication_repository import AuthenticationRepository
from app.repository.doctor_repository import DoctorRepository
from app.schemas.appointments import AppointmentRequest, RescheduleAppointment
from app.services.email_service import EmailService


class AppointmentService:
    def __init__(self):
        self.appointment_repository = AppointmentRepository()
        self.authentication_repository = AuthenticationRepository()
        self.doctor_repository = DoctorRepository()
        self.email_service = EmailService()

    def book_appointment(self, patient_id: str, appointment_request: AppointmentRequest):
        return self.appointment_repository.create_appointment(patient_id, appointment_request)

    def cancel_appointment(self, appointment_id: str, user_id: str, doctor_id: str | None):
        appointment = self.appointment_repository.get_appointment(appointment_id)

        if not appointment:
            raise HTTPException(status_code=401, detail="Appointment doesn't exists")
        if appointment.patient_id != user_id or appointment.doctor_id != doctor_id:
            raise HTTPException(status_code=401, detail="You don't have access to cancel the appointment")

        return self.appointment_repository.cancel_appointment(appointment_id)

    def update_appointment_status(self, appointment_id: str, status: AppointmentStatus, background_tasks: BackgroundTasks):
        appointment = self.appointment_repository.get_appointment(appointment_id)

        user_data = self.authentication_repository.get_user_by_id(appointment.patient_id)
        doctor_data = self.doctor_repository.get_by_id(appointment.doctor_id)
        print(f"appointment_time: {appointment.appointment_time}, Doctor_Name: {doctor_data.specialization}, User_Email: {user_data.get('email')}")
        if not appointment:
            raise HTTPException(status_code=401, detail="Appointment doesn't exists")

        updated_appointment = self.appointment_repository.update_status(appointment_id, status)

        # If confirmed, notify user via email
        if status == AppointmentStatus.CONFIRMED and updated_appointment:
            subject = "Appointment Confirmed"
            body = f"""
                   <html>
                       <body>
                           <p>Dear {user_data.get('Name')},</p>
                           <p>Your appointment scheduled on <strong>{appointment.appointment_time}</strong> has been <strong>confirmed</strong> by Dr. {doctor_data.specialization}.</p>
                           <p>Thank you for using Smart Health!</p>
                       </body>
                   </html>
                   """
            self.email_service.send_email_background(background_tasks, user_data.get('email'), subject, body)
        return updated_appointment

        # return self.appointment_repository.update_status(appointment_id, status)

    def get_your_appointments(self, user_id: str):
        return self.appointment_repository.get_appointment_history(user_id)

    def get_all_appointments(self, doc_id: str):
        return self.appointment_repository.get_appointments_doc(doc_id)

    def update_appointment_time(self, reschedule_request: RescheduleAppointment, user_id: str):
        appointment = self.appointment_repository.get_appointment(reschedule_request.appointment_id)

        if not appointment:
            raise HTTPException(status_code=401, detail="Appointment doesn't exists")
        if str(appointment.patient_id) != user_id:
            raise HTTPException(status_code=401, detail="You don't have access to reschedule appointment")

        return self.appointment_repository.update_appointment_time(reschedule_request)