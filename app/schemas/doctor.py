from datetime import time
from typing import Optional

from pydantic import Field, BaseModel

class DrRequest(BaseModel):
    specialization: str = Field(..., min_length=2, max_length=100, description="Doctor Specialization")
    qualifications: Optional[str] = Field(None, min_length=2, max_length=100, description="Doctor Qualifications (optional)")
    available_days: str = Field(..., min_length=3, max_length=100, description="Available days, e.g., 'Mon,Tue,Wed'")
    available_from: time = Field(..., description="Start time for availability (e.g., '09:00:00')")
    available_to: time = Field(..., description="End time for availability (e.g., '17:00:00')")

