from pydantic import BaseModel
from typing import List

# class Symptoms(BaseModel):
#     symptoms: List[str]

class Symptoms(BaseModel):
    age: int
    weight: int
    blood_pressure: str  # format: "120/80"
    glucose_level: int
    insulin_level: int
    smoking_habit: str  # yes or no
    symptom_1: str
    symptom_2: str
    symptom_3: str
