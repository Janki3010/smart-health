from fastapi import UploadFile

from app.repository.authentication_repository import AuthenticationRepository
from app.repository.upload_file_repository import UploadFileRepository
from app.utils.save_file import save_pdf_file


class UserService:
    def __init__(self):
        self.user_repository = AuthenticationRepository()
        self.upload_file_repository = UploadFileRepository()

    def get_user(self, user_id: str):
        return self.user_repository.get_user_by_id(user_id)

    def upload_report(self, file: UploadFile, user_id: str):
        print("File-Name:", file.filename)
        upload_entry = self.upload_file_repository.create_file_upload_entry(user_id, file.filename)
        file_path = save_pdf_file(str(upload_entry.id), file)
        self.upload_file_repository.update_file_path(upload_entry.id, file_path)
        return file_path
