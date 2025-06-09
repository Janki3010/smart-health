from fastapi import APIRouter, Request, HTTPException
from fastapi_restful.cbv import cbv
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.schemas.doctor import DrRequest
from app.services.doctore_service import DoctorService

dr_router = APIRouter(prefix="/doctor", tags=["Doctor"])

@cbv(dr_router)
class DoctorController:
    def __init__(self):
        self.doctor_service = DoctorService()

    @dr_router.post(
        "/create",
        status_code=HTTP_201_CREATED,
        summary="Create Doctor",
        description="Admin can add doctors data"
    )
    def create_dr(
            self,
            request: Request,
            createRequest: DrRequest
    ):
        user_data = getattr(request.state, "user", None)

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        # if user_data["email"] != "Junnu@gmail.com":
        if user_data["email"] != "suga@example.com":
            raise HTTPException(status_code=401, detail="You don't have access to add the data")

        return self.doctor_service.add_dr_data(createRequest)

    @dr_router.get(
        "/get_all_dr",
        status_code=HTTP_200_OK,
        summary="Get all doctors data",
        description=""
    )
    def get_dr_data(self):
        return self.doctor_service.get_dr_data()

    @dr_router.get(
        "/get_by_id",
        status_code=HTTP_200_OK,
        summary="Get dr data by id"
    )
    def get_data_by_id(self, id: str):
        return self.doctor_service.get_data_by_id(id)

    @dr_router.put(
        "/update_dr_data",
        status_code=HTTP_200_OK,
        summary="Update dr. data by id"
    )
    def update_by_id(
            self,
            id: str,
            update_request: DrRequest,
            request: Request
    ):
        user_data = getattr(request.state, "user", None)
        # if user_data["email"] != "junnu@gmail.com":
        if user_data["email"] != "suga@example.com":
            raise HTTPException(status_code=401, detail="You don't have access to update the data")

        return self.doctor_service.update_data_by_id(id, update_request)

    @dr_router.put(
        "/delete_dr_data",
        status_code=HTTP_200_OK,
        summary="Delete dr. data by id"
    )
    def delete_by_id(self, id: str, request: Request):
        user_data = getattr(request.state, "user", None)

        if user_data["email"] != "suga@example.com":
            raise HTTPException(status_code=401, detail="You don't have access to delete the data")

        return self.doctor_service.delete_data_by_id(id)


