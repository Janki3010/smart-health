from fastapi import APIRouter, Request, HTTPException, File, UploadFile
from fastapi_restful.cbv import cbv
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from app.schemas.file_validator import FileValidator
from app.services.user_service import UserService

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
        summary="Upload report",
        description="Upload Medical Reports (EX. Lab Reports, Doctor's Notes, Medication Records, General Health Reports)"
    )
    def upload_report(self, request: Request, file: UploadFile = File(...)):
        validation_errors = FileValidator.validate_pdf_file(file)
        if validation_errors:
            return JSONResponse(status_code=400, content={"success": False, "errors": validation_errors})

        user_data = getattr(request.state, "user", None)

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        return self.user_service.upload_report(file, user_data["user_id"])