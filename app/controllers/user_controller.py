import os

from fastapi import APIRouter, Request, HTTPException, File, UploadFile
from fastapi_restful.cbv import cbv
from starlette.responses import JSONResponse, FileResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from app.schemas.file_validator import FileValidator
from app.services.user_service import UserService
from app.utils.save_file import get_temporary_local_storage_path

user_router = APIRouter(prefix="/user", tags=["User"])

@cbv(user_router)
class UserController:
    def __init__(self):
        self.user_service = UserService()

    @user_router.get(
        "/me",
        status_code=HTTP_200_OK,
        summary="Get current user",
        description="Get profile info of the current user"
    )
    def get_current_user(self, request: Request):
        current_user_data = getattr(request.state, "user", None)

        if not current_user_data:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        return self.user_service.get_user(user_id=current_user_data["user_id"])

    @user_router.post(
        "/upload-report",
        status_code=HTTP_200_OK,
        summary="Upload report",
        description="Upload Medical Reports (EX. Lab Reports, Doctor's Notes, Medication Records, General Health Reports)"
    )
    def upload_report(self, request: Request, file: UploadFile = File(...)):
        user_data = getattr(request.state, "user", None)

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        role = user_data["role"]
        if role != "user":
            raise HTTPException(status_code=401, detail="You don't have access to upload the file")

        validation_errors = FileValidator.validate_pdf_file(file)
        if validation_errors:
            return JSONResponse(status_code=400, content={"success": False, "errors": validation_errors})

        return self.user_service.upload_report(file, user_data["user_id"])


    @user_router.delete(
        "/delete-report",
        status_code=HTTP_200_OK,
        summary="Delete uploaded file report"
    )
    def delete_uploaded_file(self, file_id: str, request: Request):
        user_data = getattr(request.state, "user", None)

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        role = user_data["role"]
        if role != "user":
            raise HTTPException(status_code=401, detail="You don't have access to delete the file")

        success = self.user_service.delete_uploaded_file(file_id, user_data["user_id"])

        if success:
            return {"success": True, "message": "File Deleted Successfully"}
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="File not found")

    @user_router.get(
        "/get-report",
        status_code=HTTP_200_OK,
        summary="Get Uploaded Report"
    )
    def get_uploaded_report(self, file_id: str, request: Request):
        user_data = getattr(request.state, "user", None)

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        role = user_data["role"]
        if role != "user":
            raise HTTPException(status_code=401, detail="You don't have access to get the file")

        file = self.user_service.get_report(file_id, user_data["user_id"])

        file_path=file.get("file_path")
        full_path = os.path.join(get_temporary_local_storage_path(), file_path)
        file_name=file.get("file_name")

        return FileResponse(
            path=full_path,
            filename=file_name,
            media_type="application/pdf"
        )