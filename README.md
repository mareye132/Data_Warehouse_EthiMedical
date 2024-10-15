# Data_Warehouse_EthioMedical

## Overview
This project is designed to build a comprehensive data scraping and analysis pipeline that collects and processes messages and media content from specified Telegram channels related to Ethiopian medical businesses. The data is stored in a structured format for further analysis and visualization.

## Objectives
- To gather relevant data from targeted Telegram channels.
- To clean, transform, and analyze the collected data.
- To implement object detection using YOLO for visual data insights.
- To expose the processed data through a FastAPI application for easy access and interaction.

## Directory Structure
```plaintext
my_project/
├── task-1/               # Data Scraping and Collection
│   ├── scraper.py        # Script for scraping Telegram data
│   ├── telegram_data.csv  # Collected data from Telegram channels
│   └── ...
├── task-2/               # Data Cleaning and Transformation
│   ├── cleaning.py       # Script for cleaning data
│   └── transformed_data/  # Directory for cleaned and transformed data
├── task-3/               # Object Detection Using YOLO
│   ├── yolov5/           # YOLO model files
│   ├── detect.py         # Script for detecting objects
│   └── ...
└── task-4/               # FastAPI Application
    ├── main.py           # Main FastAPI application file
    ├── database.py       # Database configuration
    ├── models.py         # SQLAlchemy models
    ├── schemas.py        # Pydantic schemas for data validation
    └── crud.py           # CRUD operations implementation
