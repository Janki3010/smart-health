from app.repository.doctor_repository import DoctorRepository
from app.schemas.doctor import DrRequest


class DoctorService:
    def __init__(self):
        self.doctor_repository = DoctorRepository()

    def add_dr_data(self, createRequest: DrRequest):
        return self.doctor_repository.add_data(createRequest)

    def get_dr_data(self):
        return self.doctor_repository.get_all_dr()

    def get_data_by_id(self, id: str):
        return self.doctor_repository.get_data_by_id(id)

    def update_data_by_id(self, id: str, update_request: DrRequest):
        return self.doctor_repository.update_dr_data(id, update_request)

    def delete_data_by_id(self, id: str):
        return self.doctor_repository.delete_data(id)