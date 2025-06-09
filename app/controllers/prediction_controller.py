from fastapi import APIRouter, Request, HTTPException
from starlette.status import HTTP_200_OK
from fastapi_restful.cbv import cbv

from app.schemas.symptom import Symptoms
from app.services.prediction_service import PredictionService

prediction_router = APIRouter(prefix="/Disease-Prediction", tags=["Disease-Prediction"])

@cbv(prediction_router)
class Prediction:
    def __init__(self):
        self.prediction_service = PredictionService()

    @prediction_router.post(
        "/",
        status_code=HTTP_200_OK,
        summary="Enter Symptoms.. will get prediction result"
    )
    def diseases_prediction(self, symptom: Symptoms, request: Request):
        user_data = getattr(request.state, "user", None)

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        return self.prediction_service.get_prediction_res(symptom, user_data["user_id"])
