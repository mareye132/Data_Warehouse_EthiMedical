# crud.py
from sqlalchemy.orm import Session
from models import YoloDetection
from schema import YoloDetectionCreate

def get_detection(db: Session, detection_id: int):
    return db.query(YoloDetection).filter(YoloDetection.id == detection_id).first()

def get_detections(db: Session, skip: int = 0, limit: int = 10):
    return db.query(YoloDetection).offset(skip).limit(limit).all()

def create_detection(db: Session, detection: YoloDetectionCreate):
    db_detection = YoloDetection(**detection.dict())
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection
