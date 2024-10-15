# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db  # This should be your database session dependency
from crud import create_detection, get_detections, get_detection  # Ensure to import the CRUD functions
from schema import YoloDetectionCreate, YoloDetection  # Import your Pydantic schemas

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ethio Medical API"}

@app.post("/detections/", response_model=YoloDetection)
def create_detection_endpoint(detection: YoloDetectionCreate, db: Session = Depends(get_db)):
    return create_detection(db=db, detection=detection)

@app.get("/detections/", response_model=list[YoloDetection])
def read_detections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_detections(db=db, skip=skip, limit=limit)

@app.get("/detections/{detection_id}", response_model=YoloDetection)
def read_detection(detection_id: int, db: Session = Depends(get_db)):
    detection = get_detection(db=db, detection_id=detection_id)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection
