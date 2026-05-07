from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    features: List[float] = Field(..., description="Iris feature vector of length 4")

class PredictResponse(BaseModel):
    predicted_class: int
    class_name: str
