import joblib
import pandas as pd

from app.repository.predication_repository import PredicationRepository
from app.schemas.symptom import Symptoms

# class PredictionService:
#     def __init__(self):
#         self.predication_repository = PredicationRepository()
#
#     def get_prediction_res(self, data: Symptoms, user_id: str):
#         model = joblib.load("/home/rl22/smart-health/app/model/disease_model.pkl")
#
#         # Same feature order as training data
#         ALL_SYMPTOMS = ["fever", "headache", "sore_throat", "cough", "fatigue"]
#
#         input_vector = [1 if symptom in data.symptoms else 0 for symptom in ALL_SYMPTOMS]
#         prediction = model.predict([input_vector])[0]
#
#         return self.predication_repository.add_prediction(data, prediction, user_id)
#
#         # return {
#         #     "symptoms_provided": data.symptoms,
#         #     "predicted_disease": prediction
#         # }


import joblib
from scipy.sparse import hstack

class PredictionService:
    def __init__(self):
        self.predication_repository = PredicationRepository()
        self.model = joblib.load("/home/rl22/smart-health/app/model/disease_model.pkl")
        self.vectorizer = joblib.load("/home/rl22/smart-health/app/model/symptom_vectorizer.pkl")
        self.label_encoder = joblib.load("/home/rl22/smart-health/app/model/label_encoder.pkl")

    def get_prediction_res(self, data: Symptoms, user_id: str):
        # Assume `data` contains all required fields: age, weight, glucose_level, etc.
        symptom_text = ' '.join([data.symptom_1, data.symptom_2, data.symptom_3])

        # Prepare numeric features
        numeric_features = [
            data.age,
            data.weight,
            data.glucose_level,
            data.insulin_level,
            int(data.blood_pressure.split("/")[0]),  # systolic
            int(data.blood_pressure.split("/")[1]),  # diastolic
            1 if data.smoking_habit.lower() == 'yes' else 0
        ]

        # Vectorize symptoms
        symptom_vector = self.vectorizer.transform([symptom_text])

        # Combine features
        final_input = hstack([numeric_features, symptom_vector])

        # Predict
        pred = self.model.predict(final_input)
        disease = self.label_encoder.inverse_transform(pred)[0]

        return self.predication_repository.add_prediction(data, disease, user_id)
        # return {
        #     "symptoms": [data.symptom_1, data.symptom_2, data.symptom_3],
        #     "predicted_disease": disease
        # }
