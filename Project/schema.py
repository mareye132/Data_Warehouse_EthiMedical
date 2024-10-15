
# schema.py
from pydantic import BaseModel

class YoloDetectionBase(BaseModel):
    confidence: float
    class_name: str
    x_min: int
    y_min: int
    x_max: int
    y_max: int

class YoloDetectionCreate(YoloDetectionBase):
    pass  # Any additional validation can be added here

class YoloDetection(YoloDetectionBase):
    id: int  # Assuming you have an ID in your database

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models
