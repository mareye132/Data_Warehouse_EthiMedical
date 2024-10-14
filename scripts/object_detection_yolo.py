import os
import logging
import pandas as pd
import cv2
import torch
import psycopg2
from pathlib import Path
from Db_connectivity import connect_to_db  # Assuming Db_connectivity is in the same directory

# Set up logging
logging.basicConfig(filename='object_detection.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_NAME = 'ethiomedical_bussiness'
TABLE_NAME = 'yolo_detections'

# YOLO model setup
MODEL_PATH = 'yolov5'  # Directory where YOLOv5 is located
MODEL_WEIGHTS = 'yolov5s.pt'  # Pre-trained weights

# Load the YOLO model
def load_yolo_model():
    try:
        model = torch.hub.load(MODEL_PATH, 'custom', path=MODEL_WEIGHTS, source='local')
        logging.info("YOLO model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Error loading YOLO model: {str(e)}")
        return None

# Collect images from a directory
def load_images_from_directory(directory):
    try:
        image_paths = list(Path(directory).glob('*.jpg'))
        logging.info(f"{len(image_paths)} images loaded from {directory}.")
        return image_paths
    except Exception as e:
        logging.error(f"Error loading images: {str(e)}")
        return []

# Run object detection on an image
def detect_objects(model, image_path):
    try:
        img = cv2.imread(str(image_path))
        results = model(img)
        detections = results.pandas().xyxy[0]  # Bounding boxes in a DataFrame
        logging.info(f"Detection successful for {image_path}.")
        return detections
    except Exception as e:
        logging.error(f"Error detecting objects in {image_path}: {str(e)}")
        return pd.DataFrame()

# Store detections into the database
def store_detections_to_db(detections, conn):
    try:
        cursor = conn.cursor()
        for _, row in detections.iterrows():
            insert_sql = f"""
            INSERT INTO {TABLE_NAME} (class, confidence, x_min, y_min, x_max, y_max) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (row['name'], row['confidence'], row['xmin'], row['ymin'], row['xmax'], row['ymax']))
        conn.commit()
        logging.info("Detections stored in the database successfully.")
    except Exception as e:
        logging.error(f"Error storing detections in the database: {str(e)}")

# Main function to run the pipeline
def main():
    # Set up the database connection
    conn = connect_to_db(DATABASE_NAME)
    if conn is None:
        logging.error("Failed to connect to the database. Exiting.")
        return

    # Load the YOLO model
    model = load_yolo_model()
    if model is None:
        logging.error("Failed to load the YOLO model. Exiting.")
        return

    # Load images
    images_dir = 'C:/Users/user/Desktop/Github/Data_Warehouse_ForEthioMedical/photos'  # Replace with actual directory path
    image_paths = load_images_from_directory(images_dir)
    if not image_paths:
        logging.error("No images found. Exiting.")
        return

    # Process each image and store detections
    for image_path in image_paths:
        detections = detect_objects(model, image_path)
        if not detections.empty:
            store_detections_to_db(detections, conn)

    # Close the database connection
    conn.close()
    logging.info("Object detection process completed successfully.")

if __name__ == "__main__":
    main()
