from app.models.medical_report import MedicalReport
from app.repository.base_repository import BaseRepository

class FileRepository(BaseRepository):
    def __init__(self):
        super().__init__(MedicalReport)

    def create_file_upload_entry(self, user_id: str, file_name: str):
        new_entry = MedicalReport(user_id=user_id, file_name=file_name, file_path="")
        return self.save(new_entry)

    def update_file_path(self, upload_id: str, file_path: str):
        self.update_by_id(upload_id, {"file_path": file_path})