# models.py
from sqlalchemy import Column, Integer, Float, String
from database import Base

class YoloDetection(Base):
    __tablename__ = "yolo_detections"

    id = Column(Integer, primary_key=True, index=True)
    confidence = Column(Float)
    class_name = Column(String)
    x_min = Column(Integer)
    y_min = Column(Integer)
    x_max = Column(Integer)
    y_max = Column(Integer)
