from fastapi import APIRouter, Request, HTTPException
from fastapi_restful.cbv import cbv
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from fastapi import BackgroundTasks

from app.models.appointment import AppointmentStatus
from app.schemas.appointments import AppointmentRequest, RescheduleAppointment
from app.services.appointment_service import AppointmentService

appointment_router = APIRouter(prefix="/appointment", tags=["Appointment"])

@cbv(appointment_router)
class Appointment:
    def __init__(self):
        self.appointment_service = AppointmentService()

    @appointment_router.post(
        "/book",
        status_code=HTTP_201_CREATED,
        summary="Book your appointment"
    )
    def book_appointment(
            self,
            request: Request,
            appointment_request: AppointmentRequest
    ):
        user_data = getattr(request.state, "user", None)
        patient_id = user_data['user_id']
        role = user_data["role"]

        if role != "user":
            raise HTTPException(status_code=401, detail="You don't have access to book appointment")

        return self.appointment_service.book_appointment(patient_id, appointment_request)


    @appointment_router.post(
        "/cancel",
        status_code=HTTP_200_OK,
        summary="Cancel appointment"
    )
    def cancel_appointment(self, appointment_id: str, request: Request, doctor_id: str | None):
        user_data = getattr(request.state, "user", None)
        return self.appointment_service.cancel_appointment(appointment_id, user_data["user_id"], doctor_id)

    @appointment_router.put(
        "/update_status",
        status_code=HTTP_200_OK,
        summary="Update Appointment Status"
    )
    def update_status(
            self,
            request: Request,
            appointment_id: str,
            status: AppointmentStatus,
            background_tasks: BackgroundTasks,
    ):
        user_data = getattr(request.state, "user", None)
        role = user_data["role"]
        if role != "doctor":
            raise HTTPException(status_code=401, detail="You don't have access to update the data")

        return self.appointment_service.update_appointment_status(appointment_id, status, background_tasks)

    @appointment_router.get(
        "/user/my_history",
        status_code=HTTP_200_OK,
        summary="Patient views their own appointments"
    )
    def get_your_appointment_history(self, request: Request):
        user_data = getattr(request.state, "user", None)
        role = user_data["role"]
        if role != "user":
            raise HTTPException(status_code=401, detail="You don't have access to view appointments")

        return self.appointment_service.get_your_appointments(user_data["user_id"])


    @appointment_router.get(
        "/doctor",
        status_code=HTTP_200_OK,
        summary="Doctor views their assigned appointments"
    )
    def get_appointment_history(self, request: Request, doc_id: str):
        user_data = getattr(request.state, "user", None)

        role = user_data["role"]
        if role != "doctor":
            raise HTTPException(status_code=401, detail="You don't have access to view appointments")

        return self.appointment_service.get_all_appointments(doc_id)

    @appointment_router.put(
        "reschedule",
        status_code=HTTP_200_OK,
        summary="Update appointment date/time"
    )
    def reschedule_appointment(self, request: Request, reschedule_request: RescheduleAppointment):
        user_data = getattr(request.state, "user", None)
        role = user_data["role"]
        if role != "user":
            raise HTTPException(status_code=401, detail="You don't have access to reschedule appointment")

        return self.appointment_service.update_appointment_time(reschedule_request, user_data["user_id"])
