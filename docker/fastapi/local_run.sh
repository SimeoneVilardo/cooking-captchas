#!/bin/bash

# Run the FastAPI application using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
