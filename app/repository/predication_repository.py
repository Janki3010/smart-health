from app.models.disease_prediction import DiseasePrediction
from app.repository.base_repository import BaseRepository
from app.schemas.symptom import Symptoms


class PredicationRepository(BaseRepository):
    def __init__(self):
        super().__init__(DiseasePrediction)

    def add_prediction(self, data: Symptoms, prediction: str,user_id: str):
        db_data = DiseasePrediction(
            user_id=user_id,
            symptoms=[data.symptom_1, data.symptom_2, data.symptom_3],
            predicted_disease=prediction
        )
        return self.save(db_data)