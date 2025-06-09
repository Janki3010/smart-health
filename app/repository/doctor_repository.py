from app.repository.base_repository import BaseRepository
from app.models.doctor import Doctor
from app.schemas.doctor import DrRequest


class DoctorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Doctor)

    def add_data(self, createRequest: DrRequest):
        db_data = Doctor(
            specialization=createRequest.specialization,
            qualifications=createRequest.qualifications,
            available_days=createRequest.available_days,
            available_from=createRequest.available_from,
            available_to=createRequest.available_to
        )
        return self.save(db_data)

    def get_all_dr(self):
        return self.get_all()

    def get_data_by_id(self, id: str):
        return self.get_by_id(id)

    def update_dr_data(self, id: str, update_request: DrRequest):
        update_data = {
            "specialization":update_request.specialization,
            "qualifications":update_request.qualifications,
            "available_days":update_request.available_days,
            "available_from":update_request.available_from,
            "available_to":update_request.available_to
        }
        return self.update_by_id(id, update_data)

    def delete_data(self, id: str):
        return self.delete_by_id(id)