
from fastapi import UploadFile, HTTPException

from app.repository.authentication_repository import AuthenticationRepository
from app.repository.file_repository import FileRepository
from app.utils.save_file import save_pdf_file, delete_stored_file


class UserService:
    def __init__(self):
        self.user_repository = AuthenticationRepository()
        self.file_repository = FileRepository()

    def get_user(self, user_id: str):
        return self.user_repository.get_user_by_id(user_id)

    def upload_report(self, file: UploadFile, user_id: str):
        print("File-Name:", file.filename)
        upload_entry = self.file_repository.create_file_upload_entry(user_id, file.filename)
        file_path = save_pdf_file(str(upload_entry.id), file)
        self.file_repository.update_file_path(upload_entry.id, file_path)
        return file_path

    def delete_uploaded_file(self, file_id: str, user_id: str):
         file_record = self.file_repository.get_by_id(file_id)

         if str(file_record.user_id) != user_id:
             raise HTTPException(status_code=401, detail="You don't have access to delete the file")

         if not file_record or not file_record.file_path:
             return False

         file_deleted = delete_stored_file(file_record.file_path)

         if not file_deleted:
             return False

         return self.file_repository.delete_by_id(file_id)

    def get_report(self, file_id, user_id: str):
        file_record = self.file_repository.get_by_id(file_id)

        if str(file_record.user_id) != user_id:
            raise HTTPException(status_code=401, detail="You don't have access to delete the file")

        if not file_record or not file_record.file_path:
            raise HTTPException(status_code=400, detail="File not found")

        return {"file_path": file_record.file_path, "file_name": file_record.file_name}